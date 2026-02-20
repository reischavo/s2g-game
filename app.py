#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2G Game - Oyun Hesabı Alışveriş Platformu
Modern ve Minimal Tasarım
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 's2g-game-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///s2g_game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Socket.IO Configuration
socketio = SocketIO(app, cors_allowed_origins="*")

# File Upload Configuration
UPLOAD_FOLDER = 'static/uploads/products'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

# Veritabanı Modelleri
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(20))
    id_card = db.Column(db.String(11))  # TC Kimlik No
    avatar = db.Column(db.String(500))
    last_ip = db.Column(db.String(50))
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    game = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))  # Hesap, Eşya, Skin vb.
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    rank = db.Column(db.String(50))
    region = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    stock = db.Column(db.Integer, default=1)
    is_sold = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, delivered, completed
    ip_address = db.Column(db.String(50))
    # Teslimat bilgileri
    account_username = db.Column(db.String(200))
    account_password = db.Column(db.String(200))
    additional_info = db.Column(db.Text)
    delivered_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(200), nullable=False)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(20))  # deposit, withdraw
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, rejected
    method = db.Column(db.String(50))  # papara, bank, crypto
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')  # open, closed, answered
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    admin_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    username = db.Column(db.String(80))  # Misafir kullanıcılar için
    message = db.Column(db.Text, nullable=False)
    sender_type = db.Column(db.String(20), default='user')  # user, admin, system
    is_read = db.Column(db.Boolean, default=False)
    session_id = db.Column(db.String(100))  # Misafir oturumları için
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Helper function to get client IP
def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr or 'Unknown'

# Helper function to log activity
def log_activity(user_id, action):
    log = ActivityLog(
        user_id=user_id,
        action=action,
        ip_address=get_client_ip(),
        user_agent=request.headers.get('User-Agent', 'Unknown')
    )
    db.session.add(log)
    db.session.commit()

# Ana Sayfa
@app.route('/')
def index():
    products = Product.query.filter_by(is_sold=False).order_by(Product.created_at.desc()).limit(12).all()
    return render_template('index_modern.html', products=products)

# Ürünler
@app.route('/products')
def products():
    game_filter = request.args.get('game', 'all')
    
    if game_filter == 'all':
        products = Product.query.filter_by(is_sold=False).all()
    else:
        products = Product.query.filter_by(is_sold=False, game=game_filter).all()
    
    return render_template('products_pro.html', products=products, current_game=game_filter)

# Ürün Detay
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Görüntülenme sayısını artır
    product.views += 1
    db.session.commit()
    
    return render_template('product_detail_pro.html', product=product)

# Kayıt
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        # Kullanıcı var mı kontrol et
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'message': 'Kullanıcı adı zaten kullanılıyor!'})
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Email zaten kullanılıyor!'})
        
        # Yeni kullanıcı oluştur
        user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            last_ip=get_client_ip()
        )
        
        db.session.add(user)
        db.session.commit()
        
        log_activity(user.id, f'Yeni kullanıcı kaydı: {user.username}')
        
        return jsonify({'success': True, 'message': 'Kayıt başarılı!'})
    
    return render_template('register_modern.html')

# Giriş
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            # Update last login info
            user.last_ip = get_client_ip()
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            log_activity(user.id, f'Kullanıcı giriş yaptı: {user.username}')
            
            return jsonify({'success': True, 'message': 'Giriş başarılı!'})
        
        return jsonify({'success': False, 'message': 'Kullanıcı adı veya şifre hatalı!'})
    
    return render_template('login_modern.html')

# Çıkış
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Profil
@app.route('/profile')
def profile():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    user = User.query.get(session.get('user_id'))
    transactions = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.created_at.desc()).limit(10).all()
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    
    # Kullanıcının ürünlerini de ekle
    user.products = Product.query.filter_by(seller_id=user.id).all()
    
    # Satıcı için bekleyen teslimatlar
    pending_deliveries = db.session.query(Order, Product).join(Product).filter(
        Product.seller_id == user.id,
        Order.status == 'pending'
    ).all()
    
    return render_template('profile_modern.html', user=user, transactions=transactions, orders=orders, pending_deliveries=pending_deliveries)

# Bakiye Yükleme
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.get_json()
        
        transaction = Transaction(
            user_id=session.get('user_id'),
            type='deposit',
            amount=float(data['amount']),
            method=data['method'],
            description=f"{data['method']} ile bakiye yükleme talebi"
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        log_activity(session.get('user_id'), f"Bakiye yükleme talebi: {data['amount']}₺ - {data['method']}")
        
        return jsonify({'success': True, 'message': 'Bakiye yükleme talebiniz alındı!'})
    
    user = User.query.get(session.get('user_id'))
    return render_template('deposit_ultra.html', user=user)

# Bakiye Çekme
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    user = User.query.get(session.get('user_id'))
    
    if request.method == 'POST':
        data = request.get_json()
        amount = float(data['amount'])
        
        if amount > user.balance:
            return jsonify({'success': False, 'message': 'Yetersiz bakiye!'})
        
        transaction = Transaction(
            user_id=session.get('user_id'),
            type='withdraw',
            amount=amount,
            method=data['method'],
            description=f"{data['method']} ile bakiye çekme talebi"
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        log_activity(session.get('user_id'), f"Bakiye çekme talebi: {amount}₺ - {data['method']}")
        
        return jsonify({'success': True, 'message': 'Bakiye çekme talebiniz alındı!'})
    
    return render_template('withdraw_ultra.html', user=user)

# Kimlik Doğrulama
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    user = User.query.get(session.get('user_id'))
    
    if request.method == 'POST':
        data = request.get_json()
        
        user.phone = data['phone']
        user.id_card = data['id_card']
        user.is_verified = True
        
        db.session.commit()
        
        log_activity(session.get('user_id'), f"Kimlik doğrulama tamamlandı")
        
        return jsonify({'success': True, 'message': 'Kimlik doğrulama başarılı!'})
    
    return render_template('verify.html', user=user)

# Admin Panel
@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    products = Product.query.order_by(Product.created_at.desc()).all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(50).all()
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).all()
    
    # İstatistikler
    total_revenue = sum(order.price for order in orders if order.status == 'completed')
    active_products = Product.query.filter_by(is_sold=False).count()
    total_views = sum(product.views for product in products)
    pending_transactions = Transaction.query.filter_by(status='pending').count()
    
    stats = {
        'total_users': len(users),
        'total_products': len(products),
        'active_products': active_products,
        'total_orders': len(orders),
        'total_revenue': total_revenue,
        'total_views': total_views,
        'pending_transactions': pending_transactions
    }
    
    # Şu anki zaman
    now = datetime.utcnow()
    
    return render_template('admin_advanced.html', users=users, products=products, orders=orders, logs=logs, stats=stats, transactions=transactions, now=now)

# Admin - Add Product
@app.route('/admin/add-product', methods=['POST'])
def add_product():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    data = request.get_json()
    
    product = Product(
        title=data['title'],
        game=data['game'],
        category=data.get('category', 'Hesap'),
        description=data['description'],
        price=float(data['price']),
        rank=data.get('rank'),
        region=data.get('region', 'TR'),
        image_url=data.get('image_url'),
        seller_id=session.get('user_id')
    )
    
    db.session.add(product)
    db.session.commit()
    
    log_activity(session.get('user_id'), f'Yeni ürün eklendi: {product.title}')
    
    return jsonify({'success': True, 'message': 'Ürün eklendi!'})

# Admin - Update Product Image
@app.route('/admin/update-image/<int:product_id>', methods=['POST'])
def update_product_image(product_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    data = request.get_json()
    product = Product.query.get_or_404(product_id)
    
    product.image_url = data.get('image_url')
    db.session.commit()
    
    log_activity(session.get('user_id'), f'Ürün görseli güncellendi: {product.title}')
    
    return jsonify({'success': True, 'message': 'Görsel güncellendi!'})

# Admin - Delete Product
@app.route('/admin/delete-product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    product = Product.query.get_or_404(product_id)
    product_title = product.title
    db.session.delete(product)
    db.session.commit()
    
    log_activity(session.get('user_id'), f'Ürün silindi: {product_title}')
    
    return jsonify({'success': True, 'message': 'Ürün silindi!'})

# Admin - Edit Product (YENİ!)
@app.route('/admin/edit-product/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    if 'title' in data:
        product.title = data['title']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = float(data['price'])
    if 'game' in data:
        product.game = data['game']
    if 'rank' in data:
        product.rank = data['rank']
    if 'region' in data:
        product.region = data['region']
    if 'image_url' in data:
        product.image_url = data['image_url']
    
    db.session.commit()
    log_activity(session.get('user_id'), f'Ürün düzenlendi: {product.title}')
    
    return jsonify({'success': True, 'message': 'Ürün güncellendi!'})

# Admin - Toggle Product Status (YENİ!)
@app.route('/admin/toggle-product/<int:product_id>', methods=['POST'])
def toggle_product(product_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    product = Product.query.get_or_404(product_id)
    product.is_sold = not product.is_sold
    db.session.commit()
    
    status = 'Satıldı' if product.is_sold else 'Aktif'
    log_activity(session.get('user_id'), f'Ürün durumu: {product.title} - {status}')
    
    return jsonify({'success': True, 'message': f'Ürün {status}!', 'is_sold': product.is_sold})

# Admin - Approve Transaction
@app.route('/admin/approve-transaction/<int:transaction_id>', methods=['POST'])
def approve_transaction(transaction_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    transaction = Transaction.query.get_or_404(transaction_id)
    user = User.query.get(transaction.user_id)
    
    if transaction.type == 'deposit':
        user.balance += transaction.amount
        transaction.status = 'completed'
    elif transaction.type == 'withdraw':
        if user.balance >= transaction.amount:
            user.balance -= transaction.amount
            transaction.status = 'completed'
        else:
            return jsonify({'success': False, 'message': 'Yetersiz bakiye!'})
    
    db.session.commit()
    
    log_activity(session.get('user_id'), f"İşlem onaylandı: #{transaction.id} - {transaction.amount}₺")
    
    return jsonify({'success': True, 'message': 'İşlem onaylandı!'})

# Admin - Reject Transaction
@app.route('/admin/reject-transaction/<int:transaction_id>', methods=['POST'])
def reject_transaction(transaction_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    transaction = Transaction.query.get_or_404(transaction_id)
    transaction.status = 'rejected'
    
    db.session.commit()
    
    log_activity(session.get('user_id'), f"İşlem reddedildi: #{transaction.id}")
    
    return jsonify({'success': True, 'message': 'İşlem reddedildi!'})

# Admin - Mark Product as Sold
@app.route('/admin/mark-sold/<int:product_id>', methods=['POST'])
def mark_sold(product_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    product = Product.query.get_or_404(product_id)
    product.is_sold = True
    
    db.session.commit()
    
    log_activity(session.get('user_id'), f"Ürün satıldı olarak işaretlendi: {product.title}")
    
    return jsonify({'success': True, 'message': 'Ürün satıldı olarak işaretlendi!'})

# Buy Product
@app.route('/buy/<int:product_id>', methods=['POST'])
def buy_product(product_id):
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'Giriş yapmalısınız!'})
    
    product = Product.query.get_or_404(product_id)
    user = User.query.get(session.get('user_id'))
    
    if product.is_sold:
        return jsonify({'success': False, 'message': 'Ürün zaten satıldı!'})
    
    # Bakiye kontrolü
    if user.balance < product.price:
        return jsonify({'success': False, 'message': 'Yetersiz bakiye! Lütfen bakiye yükleyin.'})
    
    # Bakiyeden düş
    user.balance -= product.price
    
    # Sipariş oluştur
    order = Order(
        user_id=session.get('user_id'),
        product_id=product.id,
        price=product.price,
        status='completed',
        ip_address=get_client_ip()
    )
    
    # Ürünü satıldı olarak işaretle
    product.is_sold = True
    
    db.session.add(order)
    db.session.commit()
    
    log_activity(session.get('user_id'), f'Ürün satın alındı: {product.title} - {product.price}₺')
    
    return jsonify({'success': True, 'message': 'Satın alma başarılı!', 'order_id': order.id})

# Satın Alındı Ekranı
@app.route('/order-success/<int:order_id>')
def order_success(order_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    order = Order.query.get_or_404(order_id)
    
    # Sadece sipariş sahibi görebilir
    if order.user_id != session.get('user_id'):
        return redirect(url_for('index'))
    
    product = Product.query.get(order.product_id)
    user = User.query.get(session.get('user_id'))
    
    return render_template('order_success.html', order=order, product=product, user=user)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# File Upload Route
@app.route('/upload-image', methods=['POST'])
def upload_image():
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'Giriş yapmalısınız!'})
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Dosya seçilmedi!'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Dosya seçilmedi!'})
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file
        file.save(filepath)
        
        # Return URL
        image_url = url_for('static', filename=f'uploads/products/{filename}', _external=True)
        
        log_activity(session.get('user_id'), f'Görsel yüklendi: {filename}')
        
        return jsonify({'success': True, 'image_url': image_url, 'filename': filename})
    
    return jsonify({'success': False, 'message': 'Geçersiz dosya formatı! (PNG, JPG, JPEG, GIF, WEBP)'})

# İlan Ekleme Sayfası
@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.get_json()
        
        product = Product(
            title=data['title'],
            game=data['game'],
            category=data.get('category', 'Hesap'),
            description=data['description'],
            price=float(data['price']),
            rank=data.get('rank'),
            region=data.get('region', 'TR'),
            image_url=data.get('image_url'),
            seller_id=session.get('user_id'),
            stock=1
        )
        
        db.session.add(product)
        db.session.commit()
        
        log_activity(session.get('user_id'), f'Yeni ilan eklendi: {product.title}')
        
        return jsonify({'success': True, 'message': 'İlanınız başarıyla eklendi!', 'product_id': product.id})
    
    user = User.query.get(session.get('user_id'))
    return render_template('sell.html', user=user)

# Kullanıcının İlanları
@app.route('/my-listings')
def my_listings():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    user = User.query.get(session.get('user_id'))
    products = Product.query.filter_by(seller_id=user.id).order_by(Product.created_at.desc()).all()
    
    return render_template('my_listings.html', user=user, products=products)

# Canlı Destek
@app.route('/support', methods=['GET', 'POST'])
def support():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.get_json()
        
        ticket = SupportTicket(
            user_id=session.get('user_id'),
            subject=data['subject'],
            message=data['message'],
            priority=data.get('priority', 'normal')
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        log_activity(session.get('user_id'), f'Destek talebi oluşturuldu: {ticket.subject}')
        
        return jsonify({'success': True, 'message': 'Destek talebiniz alındı!', 'ticket_id': ticket.id})
    
    user = User.query.get(session.get('user_id'))
    tickets = SupportTicket.query.filter_by(user_id=user.id).order_by(SupportTicket.created_at.desc()).all()
    
    return render_template('support.html', user=user, tickets=tickets)

# Admin - Destek Talepleri
@app.route('/admin/support')
def admin_support():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).all()
    
    return render_template('admin_support.html', tickets=tickets)

# Admin - Destek Talebi Yanıtla
@app.route('/admin/support/<int:ticket_id>/respond', methods=['POST'])
def respond_ticket(ticket_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    data = request.get_json()
    ticket = SupportTicket.query.get_or_404(ticket_id)
    
    ticket.admin_response = data['response']
    ticket.status = 'answered'
    ticket.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    log_activity(session.get('user_id'), f'Destek talebi yanıtlandı: #{ticket.id}')
    
    return jsonify({'success': True, 'message': 'Yanıt gönderildi!'})

# Admin - Destek Talebi Kapat
@app.route('/admin/support/<int:ticket_id>/close', methods=['POST'])
def close_ticket(ticket_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    ticket = SupportTicket.query.get_or_404(ticket_id)
    ticket.status = 'closed'
    ticket.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    log_activity(session.get('user_id'), f'Destek talebi kapatıldı: #{ticket.id}')
    
    return jsonify({'success': True, 'message': 'Talep kapatıldı!'})

# Admin - Kullanıcı Yönetimi
@app.route('/admin/users')
def admin_users():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

# Admin - Kullanıcı Ekle
@app.route('/admin/add-user', methods=['POST'])
def add_user():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    data = request.get_json()
    
    # Kullanıcı adı kontrolü
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'message': 'Bu kullanıcı adı zaten kullanılıyor!'})
    
    # Email kontrolü
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Bu email zaten kullanılıyor!'})
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        is_admin=data.get('is_admin', False),
        is_verified=data.get('is_verified', False),
        balance=float(data.get('balance', 0))
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    log_activity(session.get('user_id'), f'Yeni kullanıcı eklendi: {new_user.username}')
    
    return jsonify({'success': True, 'message': 'Kullanıcı eklendi!'})

# Admin - Kullanıcı Güncelle
@app.route('/admin/update-user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'balance' in data:
        user.balance = float(data['balance'])
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    if 'is_verified' in data:
        user.is_verified = data['is_verified']
    if 'password' in data and data['password']:
        user.password = generate_password_hash(data['password'])
    
    db.session.commit()
    
    log_activity(session.get('user_id'), f'Kullanıcı güncellendi: {user.username}')
    
    return jsonify({'success': True, 'message': 'Kullanıcı güncellendi!'})

# Admin - Kullanıcı Sil
@app.route('/admin/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    user = User.query.get_or_404(user_id)
    
    # Kendi hesabını silemesin
    if user.id == session.get('user_id'):
        return jsonify({'success': False, 'message': 'Kendi hesabınızı silemezsiniz!'})
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    log_activity(session.get('user_id'), f'Kullanıcı silindi: {username}')
    
    return jsonify({'success': True, 'message': 'Kullanıcı silindi!'})

# Admin - Site Ayarları
@app.route('/admin/settings')
def admin_settings():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    return render_template('admin_settings.html')

# Admin - Gelişmiş İstatistikler
@app.route('/admin/analytics')
def admin_analytics():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    # Günlük istatistikler
    today = datetime.utcnow().date()
    daily_users = User.query.filter(db.func.date(User.created_at) == today).count()
    daily_orders = Order.query.filter(db.func.date(Order.created_at) == today).count()
    daily_revenue = db.session.query(db.func.sum(Order.price)).filter(db.func.date(Order.created_at) == today).scalar() or 0
    
    # Haftalık istatistikler
    week_ago = datetime.utcnow() - timedelta(days=7)
    weekly_users = User.query.filter(User.created_at >= week_ago).count()
    weekly_orders = Order.query.filter(Order.created_at >= week_ago).count()
    weekly_revenue = db.session.query(db.func.sum(Order.price)).filter(Order.created_at >= week_ago).scalar() or 0
    
    # Aylık istatistikler
    month_ago = datetime.utcnow() - timedelta(days=30)
    monthly_users = User.query.filter(User.created_at >= month_ago).count()
    monthly_orders = Order.query.filter(Order.created_at >= month_ago).count()
    monthly_revenue = db.session.query(db.func.sum(Order.price)).filter(Order.created_at >= month_ago).scalar() or 0
    
    analytics = {
        'daily': {'users': daily_users, 'orders': daily_orders, 'revenue': daily_revenue},
        'weekly': {'users': weekly_users, 'orders': weekly_orders, 'revenue': weekly_revenue},
        'monthly': {'users': monthly_users, 'orders': monthly_orders, 'revenue': monthly_revenue}
    }
    
    return render_template('admin_analytics.html', analytics=analytics)

# ============================================
# LIVE CHAT API ENDPOINTS
# ============================================

# Chat Mesajlarını Getir
@app.route('/api/chat/messages')
def get_chat_messages():
    session_id = request.args.get('session_id')
    user_id = session.get('user_id')
    
    if user_id:
        messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.created_at.asc()).all()
    elif session_id:
        messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at.asc()).all()
    else:
        return jsonify({'success': False, 'message': 'Session ID gerekli'})
    
    messages_data = [{
        'id': msg.id,
        'message': msg.message,
        'sender_type': msg.sender_type,
        'username': msg.username,
        'created_at': msg.created_at.strftime('%H:%M')
    } for msg in messages]
    
    return jsonify({'success': True, 'messages': messages_data})

# Chat Mesajı Gönder
@app.route('/api/chat/send', methods=['POST'])
def send_chat_message():
    data = request.get_json()
    
    user_id = session.get('user_id')
    username = session.get('username', 'Misafir')
    session_id = data.get('session_id')
    message_text = data.get('message')
    
    if not message_text:
        return jsonify({'success': False, 'message': 'Mesaj boş olamaz'})
    
    # Mesajı veritabanına kaydet
    chat_message = ChatMessage(
        user_id=user_id,
        username=username,
        message=message_text,
        sender_type='user',
        session_id=session_id,
        ip_address=get_client_ip()
    )
    
    db.session.add(chat_message)
    db.session.commit()
    
    # Socket.IO ile gerçek zamanlı gönder
    socketio.emit('new_message', {
        'id': chat_message.id,
        'message': message_text,
        'sender_type': 'user',
        'username': username,
        'created_at': chat_message.created_at.strftime('%H:%M'),
        'session_id': session_id
    }, room='admin_room')
    
    log_activity(user_id or 0, f'Live chat mesajı: {message_text[:50]}...')
    
    return jsonify({
        'success': True,
        'message': 'Mesaj gönderildi',
        'data': {
            'id': chat_message.id,
            'created_at': chat_message.created_at.strftime('%H:%M')
        }
    })

# Admin - Chat Mesajı Gönder
@app.route('/api/chat/admin-send', methods=['POST'])
def admin_send_message():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    data = request.get_json()
    target_session_id = data.get('session_id')
    target_user_id = data.get('user_id')
    message_text = data.get('message')
    
    if not message_text:
        return jsonify({'success': False, 'message': 'Mesaj boş olamaz'})
    
    # Mesajı veritabanına kaydet
    chat_message = ChatMessage(
        user_id=target_user_id,
        username='Admin',
        message=message_text,
        sender_type='admin',
        session_id=target_session_id,
        ip_address=get_client_ip()
    )
    
    db.session.add(chat_message)
    db.session.commit()
    
    # Socket.IO ile kullanıcıya gönder
    socketio.emit('admin_reply', {
        'id': chat_message.id,
        'message': message_text,
        'sender_type': 'admin',
        'username': 'Admin',
        'created_at': chat_message.created_at.strftime('%H:%M')
    }, room=target_session_id or f'user_{target_user_id}')
    
    log_activity(session.get('user_id'), f'Admin chat yanıtı: {message_text[:50]}...')
    
    return jsonify({'success': True, 'message': 'Mesaj gönderildi'})

# Admin - Tüm Chat Oturumlarını Getir
@app.route('/api/chat/sessions')
def get_chat_sessions():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    # Son 24 saat içindeki benzersiz oturumları getir
    yesterday = datetime.utcnow() - timedelta(hours=24)
    
    # Kullanıcı bazlı oturumlar
    user_sessions = db.session.query(
        ChatMessage.user_id,
        User.username,
        User.email,
        db.func.count(ChatMessage.id).label('message_count'),
        db.func.max(ChatMessage.created_at).label('last_message'),
        db.func.sum(db.case((ChatMessage.is_read == False, 1), else_=0)).label('unread_count')
    ).join(User, ChatMessage.user_id == User.id)\
     .filter(ChatMessage.user_id.isnot(None))\
     .filter(ChatMessage.created_at >= yesterday)\
     .group_by(ChatMessage.user_id, User.username, User.email)\
     .all()
    
    # Misafir oturumlar
    guest_sessions = db.session.query(
        ChatMessage.session_id,
        ChatMessage.username,
        db.func.count(ChatMessage.id).label('message_count'),
        db.func.max(ChatMessage.created_at).label('last_message'),
        db.func.sum(db.case((ChatMessage.is_read == False, 1), else_=0)).label('unread_count')
    ).filter(ChatMessage.user_id.is_(None))\
     .filter(ChatMessage.session_id.isnot(None))\
     .filter(ChatMessage.created_at >= yesterday)\
     .group_by(ChatMessage.session_id, ChatMessage.username)\
     .all()
    
    sessions_data = []
    
    # Kullanıcı oturumları
    for session_item in user_sessions:
        sessions_data.append({
            'type': 'user',
            'user_id': session_item.user_id,
            'username': session_item.username,
            'email': session_item.email,
            'message_count': session_item.message_count,
            'last_message': session_item.last_message.strftime('%d.%m.%Y %H:%M'),
            'unread_count': session_item.unread_count or 0
        })
    
    # Misafir oturumları
    for session_item in guest_sessions:
        sessions_data.append({
            'type': 'guest',
            'session_id': session_item.session_id,
            'username': session_item.username or 'Misafir',
            'email': None,
            'message_count': session_item.message_count,
            'last_message': session_item.last_message.strftime('%d.%m.%Y %H:%M'),
            'unread_count': session_item.unread_count or 0
        })
    
    # Son mesaja göre sırala
    sessions_data.sort(key=lambda x: x['last_message'], reverse=True)
    
    return jsonify({'success': True, 'sessions': sessions_data})

# Admin - Belirli Oturumun Mesajlarını Getir
@app.route('/api/chat/session-messages')
def get_session_messages():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    user_id = request.args.get('user_id')
    session_id = request.args.get('session_id')
    
    if user_id:
        messages = ChatMessage.query.filter_by(user_id=int(user_id)).order_by(ChatMessage.created_at.asc()).all()
        # Okundu olarak işaretle
        for msg in messages:
            if not msg.is_read and msg.sender_type == 'user':
                msg.is_read = True
        db.session.commit()
    elif session_id:
        messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at.asc()).all()
        # Okundu olarak işaretle
        for msg in messages:
            if not msg.is_read and msg.sender_type == 'user':
                msg.is_read = True
        db.session.commit()
    else:
        return jsonify({'success': False, 'message': 'User ID veya Session ID gerekli'})
    
    messages_data = [{
        'id': msg.id,
        'message': msg.message,
        'sender_type': msg.sender_type,
        'username': msg.username,
        'created_at': msg.created_at.strftime('%d.%m.%Y %H:%M:%S')
    } for msg in messages]
    
    return jsonify({'success': True, 'messages': messages_data})

# ============================================
# SOCKET.IO EVENT HANDLERS
# ============================================

@socketio.on('connect')
def handle_connect():
    print(f'✅ Client connected: {request.sid}')
    
    # Admin ise admin room'a ekle
    if session.get('is_admin'):
        join_room('admin_room')
        print(f'👑 Admin joined admin_room')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'❌ Client disconnected: {request.sid}')

@socketio.on('join_chat')
def handle_join_chat(data):
    room = data.get('session_id') or f"user_{data.get('user_id')}"
    join_room(room)
    print(f'📥 User joined room: {room}')

@socketio.on('leave_chat')
def handle_leave_chat(data):
    room = data.get('session_id') or f"user_{data.get('user_id')}"
    leave_room(room)
    print(f'📤 User left room: {room}')

# ============================================
# SELLER DELIVERY ROUTES
# ============================================

@app.route('/seller/delivery/<int:order_id>')
def seller_delivery(order_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    order = Order.query.get_or_404(order_id)
    product = Product.query.get(order.product_id)
    buyer = User.query.get(order.user_id)
    
    # Sadece satıcı görebilir
    if product.seller_id != session.get('user_id'):
        return redirect(url_for('profile'))
    
    # Zaten teslim edilmişse
    if order.status == 'delivered':
        return redirect(url_for('profile'))
    
    return render_template('seller_delivery.html', order=order, product=product, buyer=buyer)

@app.route('/seller/deliver', methods=['POST'])
def seller_deliver():
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'Giriş yapmalısınız!'})
    
    data = request.get_json()
    order_id = data.get('order_id')
    
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'success': False, 'message': 'Sipariş bulunamadı!'})
    
    product = Product.query.get(order.product_id)
    
    # Sadece satıcı teslim edebilir
    if product.seller_id != session.get('user_id'):
        return jsonify({'success': False, 'message': 'Bu siparişi teslim etme yetkiniz yok!'})
    
    # Teslimat bilgilerini kaydet
    order.account_username = data.get('account_username')
    order.account_password = data.get('account_password')
    order.additional_info = data.get('additional_info')
    order.status = 'delivered'
    order.delivered_at = datetime.utcnow()
    
    # Satıcıya bakiye ekle (%90 komisyon)
    seller = User.query.get(product.seller_id)
    seller.balance += order.price * 0.9
    
    db.session.commit()
    
    log_activity(session.get('user_id'), f'Sipariş #{order.id} teslim edildi')
    
    return jsonify({'success': True, 'message': 'Teslimat başarıyla tamamlandı!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('✅ Veritabanı oluşturuldu!')
        
        # İlk admin kullanıcısı oluştur
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@s2ggame.com',
                password=generate_password_hash('admin123'),
                is_admin=True,
                balance=0.0
            )
            db.session.add(admin_user)
            db.session.commit()
            print('✅ Admin kullanıcısı oluşturuldu! (admin / admin123)')
    
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)
