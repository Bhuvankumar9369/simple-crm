from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os

# Custom Jinja2 filters
def from_json(value):
    """Convert JSON string to Python object"""
    if value is None:
        return []
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []

def safe_json_load(value):
    """Safely load JSON data"""
    if value is None:
        return {}
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return {}

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database configuration - use PostgreSQL on Heroku, SQLite locally
if os.environ.get('DATABASE_URL'):
    # Heroku PostgreSQL
    database_url = os.environ.get('DATABASE_URL')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register custom Jinja2 filters
app.jinja_env.filters['from_json'] = from_json
app.jinja_env.filters['safe_json'] = safe_json_load

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, manager, user
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Permission Set Model
class PermissionSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Permission Set Permissions Model
class PermissionSetPermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    permission_set_id = db.Column(db.Integer, db.ForeignKey('permission_set.id'), nullable=False)
    object_type = db.Column(db.String(50), nullable=False)  # 'contact', 'account', 'opportunity', 'lead', 'custom_object'
    object_id = db.Column(db.Integer, nullable=True)  # For custom objects, this is the custom_object.id
    can_view = db.Column(db.Boolean, default=True)
    can_create = db.Column(db.Boolean, default=False)
    can_edit = db.Column(db.Boolean, default=False)
    can_delete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# User Permissions Model
class UserPermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    object_type = db.Column(db.String(50), nullable=False)  # 'contact', 'account', 'opportunity', 'lead', 'custom_object'
    object_id = db.Column(db.Integer, nullable=True)  # For custom objects, this is the custom_object.id
    can_view = db.Column(db.Boolean, default=True)
    can_create = db.Column(db.Boolean, default=False)
    can_edit = db.Column(db.Boolean, default=False)
    can_delete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# User Permission Set Assignment Model
class UserPermissionSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    permission_set_id = db.Column(db.Integer, db.ForeignKey('permission_set.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Standard Objects
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    title = db.Column(db.String(100))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50))
    website = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    annual_revenue = db.Column(db.Float)
    employees = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    amount = db.Column(db.Float)
    stage = db.Column(db.String(50))
    close_date = db.Column(db.Date)
    probability = db.Column(db.Integer)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    status = db.Column(db.String(50), default='New')
    source = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Custom Objects System
class CustomObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    label = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    fields = db.Column(db.Text)  # JSON string of field definitions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CustomRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('custom_object.id'))
    data = db.Column(db.Text)  # JSON string of field values
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Permission helper functions
def has_permission(user, object_type, object_id=None, permission='view'):
    """Check if user has permission for a specific object type and permission level."""
    if user.role == 'admin':
        return True
    
    permission_map = {
        'view': 'can_view',
        'create': 'can_create', 
        'edit': 'can_edit',
        'delete': 'can_delete'
    }
    
    permission_field = permission_map.get(permission, 'can_view')
    
    # First check direct user permissions
    query = UserPermission.query.filter_by(
        user_id=user.id,
        object_type=object_type,
        object_id=object_id
    )
    
    if object_id is None:
        # For standard objects, check general permissions
        query = query.filter_by(object_id=None)
    
    user_permission = query.first()
    
    if user_permission:
        return getattr(user_permission, permission_field, False)
    
    # If no direct permission, check permission sets
    user_permission_sets = UserPermissionSet.query.filter_by(user_id=user.id).all()
    
    for user_ps in user_permission_sets:
        permission_set = PermissionSet.query.get(user_ps.permission_set_id)
        if permission_set and permission_set.is_active:
            # Check permission set permissions
            ps_query = PermissionSetPermission.query.filter_by(
                permission_set_id=permission_set.id,
                object_type=object_type,
                object_id=object_id
            )
            
            if object_id is None:
                ps_query = ps_query.filter_by(object_id=None)
            
            ps_permission = ps_query.first()
            
            if ps_permission:
                return getattr(ps_permission, permission_field, False)
    
    return False

def get_user_permissions(user):
    """Get all permissions for a user."""
    if user.role == 'admin':
        return {
            'contact': {'view': True, 'create': True, 'edit': True, 'delete': True},
            'account': {'view': True, 'create': True, 'edit': True, 'delete': True},
            'opportunity': {'view': True, 'create': True, 'edit': True, 'delete': True},
            'lead': {'view': True, 'create': True, 'edit': True, 'delete': True},
            'custom_object': {'view': True, 'create': True, 'edit': True, 'delete': True}
        }
    
    permissions = {}
    user_perms = UserPermission.query.filter_by(user_id=user.id).all()
    
    for perm in user_perms:
        if perm.object_type not in permissions:
            permissions[perm.object_type] = {}
        
        permissions[perm.object_type][perm.object_id] = {
            'view': perm.can_view,
            'create': perm.can_create,
            'edit': perm.can_edit,
            'delete': perm.can_delete
        }
    
    return permissions

# Register template functions
app.jinja_env.globals['has_permission'] = has_permission

# Routes
@app.route('/')
@login_required
def dashboard():
    contacts_count = Contact.query.count()
    accounts_count = Account.query.count()
    opportunities_count = Opportunity.query.count()
    leads_count = Lead.query.count()
    custom_objects_count = CustomObject.query.count()
    
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    recent_opportunities = Opportunity.query.order_by(Opportunity.created_at.desc()).limit(5).all()
    recent_custom_objects = CustomObject.query.order_by(CustomObject.created_at.desc()).limit(3).all()
    
    return render_template('dashboard.html', 
                         contacts_count=contacts_count,
                         accounts_count=accounts_count,
                         opportunities_count=opportunities_count,
                         leads_count=leads_count,
                         custom_objects_count=custom_objects_count,
                         recent_contacts=recent_contacts,
                         recent_opportunities=recent_opportunities,
                         recent_custom_objects=recent_custom_objects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# User Management Routes
@app.route('/users')
@login_required
def users():
    if not has_permission(current_user, 'user', permission='view'):
        flash('You do not have permission to view users.')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
@login_required
def new_user():
    if not has_permission(current_user, 'user', permission='create'):
        flash('You do not have permission to create users.')
        return redirect(url_for('users'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('user_form.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return render_template('user_form.html')
        
        user = User(
            username=username, 
            email=email, 
            password_hash=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()
        
        # Set default permissions based on role
        set_default_permissions(user)
        
        flash('User created successfully!')
        return redirect(url_for('users'))
    
    return render_template('user_form.html')

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if not has_permission(current_user, 'user', permission='edit'):
        flash('You do not have permission to edit users.')
        return redirect(url_for('users'))
    
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        user.is_active = 'is_active' in request.form
        
        if request.form.get('password'):
            user.password_hash = generate_password_hash(request.form['password'])
        
        db.session.commit()
        flash('User updated successfully!')
        return redirect(url_for('users'))
    
    return render_template('user_form.html', user=user)

@app.route('/users/<int:id>/permissions', methods=['GET', 'POST'])
@login_required
def user_permissions(id):
    if not has_permission(current_user, 'user', permission='edit'):
        flash('You do not have permission to manage user permissions.')
        return redirect(url_for('users'))
    
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        # Clear existing permissions
        UserPermission.query.filter_by(user_id=user.id).delete()
        
        # Standard objects permissions
        standard_objects = ['contact', 'account', 'opportunity', 'lead']
        for obj_type in standard_objects:
            can_view = f'{obj_type}_view' in request.form
            can_create = f'{obj_type}_create' in request.form
            can_edit = f'{obj_type}_edit' in request.form
            can_delete = f'{obj_type}_delete' in request.form
            
            if can_view or can_create or can_edit or can_delete:
                permission = UserPermission(
                    user_id=user.id,
                    object_type=obj_type,
                    can_view=can_view,
                    can_create=can_create,
                    can_edit=can_edit,
                    can_delete=can_delete
                )
                db.session.add(permission)
        
        # Custom objects permissions
        custom_objects = CustomObject.query.all()
        for custom_obj in custom_objects:
            can_view = f'custom_{custom_obj.id}_view' in request.form
            can_create = f'custom_{custom_obj.id}_create' in request.form
            can_edit = f'custom_{custom_obj.id}_edit' in request.form
            can_delete = f'custom_{custom_obj.id}_delete' in request.form
            
            if can_view or can_create or can_edit or can_delete:
                permission = UserPermission(
                    user_id=user.id,
                    object_type='custom_object',
                    object_id=custom_obj.id,
                    can_view=can_view,
                    can_create=can_create,
                    can_edit=can_edit,
                    can_delete=can_delete
                )
                db.session.add(permission)
        
        db.session.commit()
        flash('User permissions updated successfully!')
        return redirect(url_for('users'))
    
    # Get current permissions
    user_permissions = UserPermission.query.filter_by(user_id=user.id).all()
    permissions_dict = {}
    
    for perm in user_permissions:
        key = f"{perm.object_type}_{perm.object_id or 'general'}"
        permissions_dict[key] = {
            'view': perm.can_view,
            'create': perm.can_create,
            'edit': perm.can_edit,
            'delete': perm.can_delete
        }
    
    custom_objects = CustomObject.query.all()
    return render_template('user_permissions.html', user=user, permissions=permissions_dict, custom_objects=custom_objects)

def set_default_permissions(user):
    """Set default permissions for a new user based on their role."""
    if user.role == 'admin':
        return  # Admin has all permissions
    
    # Set basic view permissions for standard objects
    standard_objects = ['contact', 'account', 'opportunity', 'lead']
    for obj_type in standard_objects:
        permission = UserPermission(
            user_id=user.id,
            object_type=obj_type,
            can_view=True,
            can_create=False,
            can_edit=False,
            can_delete=False
        )
        db.session.add(permission)
    
    db.session.commit()

# Permission Set Routes
@app.route('/permission-sets')
@login_required
def permission_sets():
    if not has_permission(current_user, 'user', permission='view'):
        flash('You do not have permission to view permission sets.')
        return redirect(url_for('dashboard'))
    
    permission_sets = PermissionSet.query.all()
    return render_template('permission_sets.html', permission_sets=permission_sets)

@app.route('/permission-sets/new', methods=['GET', 'POST'])
@login_required
def new_permission_set():
    if not has_permission(current_user, 'user', permission='create'):
        flash('You do not have permission to create permission sets.')
        return redirect(url_for('permission_sets'))
    
    if request.method == 'POST':
        permission_set = PermissionSet(
            name=request.form['name'],
            description=request.form['description'],
            is_active='is_active' in request.form
        )
        db.session.add(permission_set)
        db.session.commit()
        
        # Add permissions to the permission set
        standard_objects = ['contact', 'account', 'opportunity', 'lead']
        for obj_type in standard_objects:
            can_view = f'{obj_type}_view' in request.form
            can_create = f'{obj_type}_create' in request.form
            can_edit = f'{obj_type}_edit' in request.form
            can_delete = f'{obj_type}_delete' in request.form
            
            if can_view or can_create or can_edit or can_delete:
                permission = PermissionSetPermission(
                    permission_set_id=permission_set.id,
                    object_type=obj_type,
                    can_view=can_view,
                    can_create=can_create,
                    can_edit=can_edit,
                    can_delete=can_delete
                )
                db.session.add(permission)
        
        # Custom objects permissions
        custom_objects = CustomObject.query.all()
        for custom_obj in custom_objects:
            can_view = f'custom_{custom_obj.id}_view' in request.form
            can_create = f'custom_{custom_obj.id}_create' in request.form
            can_edit = f'custom_{custom_obj.id}_edit' in request.form
            can_delete = f'custom_{custom_obj.id}_delete' in request.form
            
            if can_view or can_create or can_edit or can_delete:
                permission = PermissionSetPermission(
                    permission_set_id=permission_set.id,
                    object_type='custom_object',
                    object_id=custom_obj.id,
                    can_view=can_view,
                    can_create=can_create,
                    can_edit=can_edit,
                    can_delete=can_delete
                )
                db.session.add(permission)
        
        db.session.commit()
        flash('Permission set created successfully!')
        return redirect(url_for('permission_sets'))
    
    custom_objects = CustomObject.query.all()
    return render_template('permission_set_form.html', custom_objects=custom_objects, permissions={})

@app.route('/permission-sets/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_permission_set(id):
    if not has_permission(current_user, 'user', permission='edit'):
        flash('You do not have permission to edit permission sets.')
        return redirect(url_for('permission_sets'))
    
    permission_set = PermissionSet.query.get_or_404(id)
    
    if request.method == 'POST':
        permission_set.name = request.form['name']
        permission_set.description = request.form['description']
        permission_set.is_active = 'is_active' in request.form
        
        # Clear existing permissions
        PermissionSetPermission.query.filter_by(permission_set_id=permission_set.id).delete()
        
        # Standard objects permissions
        standard_objects = ['contact', 'account', 'opportunity', 'lead']
        for obj_type in standard_objects:
            can_view = f'{obj_type}_view' in request.form
            can_create = f'{obj_type}_create' in request.form
            can_edit = f'{obj_type}_edit' in request.form
            can_delete = f'{obj_type}_delete' in request.form
            
            if can_view or can_create or can_edit or can_delete:
                permission = PermissionSetPermission(
                    permission_set_id=permission_set.id,
                    object_type=obj_type,
                    can_view=can_view,
                    can_create=can_create,
                    can_edit=can_edit,
                    can_delete=can_delete
                )
                db.session.add(permission)
        
        # Custom objects permissions
        custom_objects = CustomObject.query.all()
        for custom_obj in custom_objects:
            can_view = f'custom_{custom_obj.id}_view' in request.form
            can_create = f'custom_{custom_obj.id}_create' in request.form
            can_edit = f'custom_{custom_obj.id}_edit' in request.form
            can_delete = f'custom_{custom_obj.id}_delete' in request.form
            
            if can_view or can_create or can_edit or can_delete:
                permission = PermissionSetPermission(
                    permission_set_id=permission_set.id,
                    object_type='custom_object',
                    object_id=custom_obj.id,
                    can_view=can_view,
                    can_create=can_create,
                    can_edit=can_edit,
                    can_delete=can_delete
                )
                db.session.add(permission)
        
        db.session.commit()
        flash('Permission set updated successfully!')
        return redirect(url_for('permission_sets'))
    
    # Get current permissions
    permissions = PermissionSetPermission.query.filter_by(permission_set_id=permission_set.id).all()
    permissions_dict = {}
    
    for perm in permissions:
        key = f"{perm.object_type}_{perm.object_id or 'general'}"
        permissions_dict[key] = {
            'view': perm.can_view,
            'create': perm.can_create,
            'edit': perm.can_edit,
            'delete': perm.can_delete
        }
    
    custom_objects = CustomObject.query.all()
    return render_template('permission_set_form.html', permission_set=permission_set, permissions=permissions_dict, custom_objects=custom_objects)

@app.route('/users/<int:id>/assign-permission-sets', methods=['GET', 'POST'])
@login_required
def assign_permission_sets(id):
    if not has_permission(current_user, 'user', permission='edit'):
        flash('You do not have permission to assign permission sets.')
        return redirect(url_for('users'))
    
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        # Clear existing permission set assignments
        UserPermissionSet.query.filter_by(user_id=user.id).delete()
        
        # Assign selected permission sets
        selected_sets = request.form.getlist('permission_sets')
        for set_id in selected_sets:
            assignment = UserPermissionSet(
                user_id=user.id,
                permission_set_id=int(set_id),
                assigned_by=current_user.id
            )
            db.session.add(assignment)
        
        db.session.commit()
        flash('Permission sets assigned successfully!')
        return redirect(url_for('users'))
    
    # Get available permission sets
    available_sets = PermissionSet.query.filter_by(is_active=True).all()
    
    # Get current assignments
    current_assignments = UserPermissionSet.query.filter_by(user_id=user.id).all()
    assigned_set_ids = [assignment.permission_set_id for assignment in current_assignments]
    
    return render_template('assign_permission_sets.html', user=user, available_sets=available_sets, assigned_set_ids=assigned_set_ids)

# Contact routes
@app.route('/contacts')
@login_required
def contacts():
    if not has_permission(current_user, 'contact', permission='view'):
        flash('You do not have permission to view contacts.')
        return redirect(url_for('dashboard'))
    
    contacts = Contact.query.all()
    return render_template('contacts.html', contacts=contacts)

@app.route('/contacts/new', methods=['GET', 'POST'])
@login_required
def new_contact():
    if not has_permission(current_user, 'contact', permission='create'):
        flash('You do not have permission to create contacts.')
        return redirect(url_for('contacts'))
    
    if request.method == 'POST':
        contact = Contact(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            phone=request.form['phone'],
            company=request.form['company'],
            title=request.form['title'],
            address=request.form['address']
        )
        db.session.add(contact)
        db.session.commit()
        flash('Contact created successfully!')
        return redirect(url_for('contacts'))
    
    return render_template('contact_form.html')

@app.route('/contacts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        contact.first_name = request.form['first_name']
        contact.last_name = request.form['last_name']
        contact.email = request.form['email']
        contact.phone = request.form['phone']
        contact.company = request.form['company']
        contact.title = request.form['title']
        contact.address = request.form['address']
        db.session.commit()
        flash('Contact updated successfully!')
        return redirect(url_for('contacts'))
    
    return render_template('contact_form.html', contact=contact)

@app.route('/contacts/<int:id>/delete')
@login_required
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully!')
    return redirect(url_for('contacts'))

# Account routes
@app.route('/accounts')
@login_required
def accounts():
    accounts = Account.query.all()
    return render_template('accounts.html', accounts=accounts)

@app.route('/accounts/new', methods=['GET', 'POST'])
@login_required
def new_account():
    if request.method == 'POST':
        account = Account(
            name=request.form['name'],
            industry=request.form['industry'],
            website=request.form['website'],
            phone=request.form['phone'],
            address=request.form['address'],
            annual_revenue=float(request.form['annual_revenue']) if request.form['annual_revenue'] else None,
            employees=int(request.form['employees']) if request.form['employees'] else None
        )
        db.session.add(account)
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for('accounts'))
    
    return render_template('account_form.html')

@app.route('/accounts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_account(id):
    account = Account.query.get_or_404(id)
    if request.method == 'POST':
        account.name = request.form['name']
        account.industry = request.form['industry']
        account.website = request.form['website']
        account.phone = request.form['phone']
        account.address = request.form['address']
        account.annual_revenue = float(request.form['annual_revenue']) if request.form['annual_revenue'] else None
        account.employees = int(request.form['employees']) if request.form['employees'] else None
        db.session.commit()
        flash('Account updated successfully!')
        return redirect(url_for('accounts'))
    
    return render_template('account_form.html', account=account)

@app.route('/accounts/<int:id>/delete')
@login_required
def delete_account(id):
    account = Account.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    flash('Account deleted successfully!')
    return redirect(url_for('accounts'))

# Opportunity routes
@app.route('/opportunities')
@login_required
def opportunities():
    opportunities = Opportunity.query.all()
    return render_template('opportunities.html', opportunities=opportunities)

@app.route('/opportunities/new', methods=['GET', 'POST'])
@login_required
def new_opportunity():
    if request.method == 'POST':
        opportunity = Opportunity(
            name=request.form['name'],
            account_id=int(request.form['account_id']) if request.form['account_id'] else None,
            contact_id=int(request.form['contact_id']) if request.form['contact_id'] else None,
            amount=float(request.form['amount']) if request.form['amount'] else None,
            stage=request.form['stage'],
            close_date=datetime.strptime(request.form['close_date'], '%Y-%m-%d').date() if request.form['close_date'] else None,
            probability=int(request.form['probability']) if request.form['probability'] else None,
            description=request.form['description']
        )
        db.session.add(opportunity)
        db.session.commit()
        flash('Opportunity created successfully!')
        return redirect(url_for('opportunities'))
    
    accounts = Account.query.all()
    contacts = Contact.query.all()
    return render_template('opportunity_form.html', accounts=accounts, contacts=contacts)

@app.route('/opportunities/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_opportunity(id):
    opportunity = Opportunity.query.get_or_404(id)
    if request.method == 'POST':
        opportunity.name = request.form['name']
        opportunity.account_id = int(request.form['account_id']) if request.form['account_id'] else None
        opportunity.contact_id = int(request.form['contact_id']) if request.form['contact_id'] else None
        opportunity.amount = float(request.form['amount']) if request.form['amount'] else None
        opportunity.stage = request.form['stage']
        opportunity.close_date = datetime.strptime(request.form['close_date'], '%Y-%m-%d').date() if request.form['close_date'] else None
        opportunity.probability = int(request.form['probability']) if request.form['probability'] else None
        opportunity.description = request.form['description']
        db.session.commit()
        flash('Opportunity updated successfully!')
        return redirect(url_for('opportunities'))
    
    accounts = Account.query.all()
    contacts = Contact.query.all()
    return render_template('opportunity_form.html', opportunity=opportunity, accounts=accounts, contacts=contacts)

@app.route('/opportunities/<int:id>/delete')
@login_required
def delete_opportunity(id):
    opportunity = Opportunity.query.get_or_404(id)
    db.session.delete(opportunity)
    db.session.commit()
    flash('Opportunity deleted successfully!')
    return redirect(url_for('opportunities'))

# Lead routes
@app.route('/leads')
@login_required
def leads():
    leads = Lead.query.all()
    return render_template('leads.html', leads=leads)

@app.route('/leads/new', methods=['GET', 'POST'])
@login_required
def new_lead():
    if request.method == 'POST':
        lead = Lead(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            phone=request.form['phone'],
            company=request.form['company'],
            status=request.form['status'],
            source=request.form['source'],
            notes=request.form['notes']
        )
        db.session.add(lead)
        db.session.commit()
        flash('Lead created successfully!')
        return redirect(url_for('leads'))
    
    return render_template('lead_form.html')

@app.route('/leads/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lead(id):
    lead = Lead.query.get_or_404(id)
    if request.method == 'POST':
        lead.first_name = request.form['first_name']
        lead.last_name = request.form['last_name']
        lead.email = request.form['email']
        lead.phone = request.form['phone']
        lead.company = request.form['company']
        lead.status = request.form['status']
        lead.source = request.form['source']
        lead.notes = request.form['notes']
        db.session.commit()
        flash('Lead updated successfully!')
        return redirect(url_for('leads'))
    
    return render_template('lead_form.html', lead=lead)

@app.route('/leads/<int:id>/delete')
@login_required
def delete_lead(id):
    lead = Lead.query.get_or_404(id)
    db.session.delete(lead)
    db.session.commit()
    flash('Lead deleted successfully!')
    return redirect(url_for('leads'))

# Custom Objects routes
@app.route('/custom-objects')
@login_required
def custom_objects():
    objects = CustomObject.query.all()
    return render_template('custom_objects.html', objects=objects)

@app.route('/custom-objects/new', methods=['GET', 'POST'])
@login_required
def new_custom_object():
    if request.method == 'POST':
        fields = []
        field_names = request.form.getlist('field_name[]')
        field_types = request.form.getlist('field_type[]')
        field_labels = request.form.getlist('field_label[]')
        
        for i in range(len(field_names)):
            if field_names[i]:
                fields.append({
                    'name': field_names[i],
                    'type': field_types[i],
                    'label': field_labels[i]
                })
        
        custom_object = CustomObject(
            name=request.form['name'],
            label=request.form['label'],
            description=request.form['description'],
            fields=json.dumps(fields)
        )
        db.session.add(custom_object)
        db.session.commit()
        flash('Custom object created successfully!')
        return redirect(url_for('custom_objects'))
    
    return render_template('custom_object_form.html')

@app.route('/custom-objects/<int:id>/records')
@login_required
def custom_records(id):
    custom_object = CustomObject.query.get_or_404(id)
    records = CustomRecord.query.filter_by(object_id=id).all()
    fields = safe_json_load(custom_object.fields)
    return render_template('custom_records.html', custom_object=custom_object, records=records, fields=fields)

@app.route('/custom-objects/<int:id>/records/new', methods=['GET', 'POST'])
@login_required
def new_custom_record(id):
    custom_object = CustomObject.query.get_or_404(id)
    fields = safe_json_load(custom_object.fields)
    
    if request.method == 'POST':
        data = {}
        for field in fields:
            data[field['name']] = request.form.get(field['name'], '')
        
        record = CustomRecord(
            object_id=id,
            data=json.dumps(data)
        )
        db.session.add(record)
        db.session.commit()
        flash('Record created successfully!')
        return redirect(url_for('custom_records', id=id))
    
    return render_template('custom_record_form.html', custom_object=custom_object, fields=fields)

def initialize_database():
    """Initialize the database with tables and sample data."""
    print("🗄️  Initializing Simple CRM Database...")
    
    with app.app_context():
        # Create all tables (don't drop on Heroku to preserve data)
        print("🏗️  Creating database tables...")
        db.create_all()
        
        # Create admin user
        print("👤 Creating admin user...")
        admin = User(
            username='admin',
            email='admin@crm.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        
        # Create sample users
        print("👥 Creating sample users...")
        users = [
            User(username='manager1', email='manager1@crm.com', password_hash=generate_password_hash('manager123'), role='manager'),
            User(username='user1', email='user1@crm.com', password_hash=generate_password_hash('user123'), role='user'),
            User(username='user2', email='user2@crm.com', password_hash=generate_password_hash('user123'), role='user')
        ]
        db.session.add_all(users)
        db.session.commit()
        print(f"✅ Created {len(users)} sample users")
        
        # Add sample data
        print("📊 Adding sample data...")
        
        # Sample Contacts
        contacts = [
            Contact(first_name='John', last_name='Doe', email='john.doe@example.com', 
                   phone='+1-555-0101', company='TechCorp', title='CEO'),
            Contact(first_name='Jane', last_name='Smith', email='jane.smith@example.com', 
                   phone='+1-555-0102', company='InnovateInc', title='CTO'),
            Contact(first_name='Mike', last_name='Johnson', email='mike.johnson@example.com', 
                   phone='+1-555-0103', company='GlobalTech', title='VP Sales'),
            Contact(first_name='Sarah', last_name='Williams', email='sarah.williams@example.com', 
                   phone='+1-555-0104', company='StartupXYZ', title='Marketing Director'),
            Contact(first_name='David', last_name='Brown', email='david.brown@example.com', 
                   phone='+1-555-0105', company='EnterpriseCo', title='Product Manager')
        ]
        db.session.add_all(contacts)
        db.session.commit()
        print(f"✅ Added {len(contacts)} sample contacts")
        
        # Sample Accounts
        accounts = [
            Account(name='TechCorp', industry='Technology', website='https://techcorp.com', 
                   phone='+1-555-0201', annual_revenue=5000000, employees=150),
            Account(name='InnovateInc', industry='Technology', website='https://innovateinc.com', 
                   phone='+1-555-0202', annual_revenue=2500000, employees=75),
            Account(name='GlobalTech', industry='Technology', website='https://globaltech.com', 
                   phone='+1-555-0203', annual_revenue=10000000, employees=300),
            Account(name='StartupXYZ', industry='Technology', website='https://startupxyz.com', 
                   phone='+1-555-0204', annual_revenue=500000, employees=25),
            Account(name='EnterpriseCo', industry='Manufacturing', website='https://enterpriseco.com', 
                   phone='+1-555-0205', annual_revenue=20000000, employees=500)
        ]
        db.session.add_all(accounts)
        db.session.commit()
        print(f"✅ Added {len(accounts)} sample accounts")
        
        # Sample Opportunities
        opportunities = [
            Opportunity(name='Enterprise Software License', account_id=1, contact_id=1, 
                       amount=50000, stage='Proposal', probability=75, 
                       description='Multi-year software license for enterprise deployment'),
            Opportunity(name='Cloud Migration Project', account_id=2, contact_id=2, 
                       amount=150000, stage='Negotiation', probability=60, 
                       description='Complete cloud infrastructure migration'),
            Opportunity(name='Custom Development', account_id=3, contact_id=3, 
                       amount=75000, stage='Qualification', probability=40, 
                       description='Custom software development for sales automation'),
            Opportunity(name='Consulting Services', account_id=4, contact_id=4, 
                       amount=25000, stage='Prospecting', probability=20, 
                       description='Technical consulting and implementation services'),
            Opportunity(name='System Integration', account_id=5, contact_id=5, 
                       amount=100000, stage='Closed Won', probability=100, 
                       description='Integration of existing systems with new platform')
        ]
        db.session.add_all(opportunities)
        db.session.commit()
        print(f"✅ Added {len(opportunities)} sample opportunities")
        
        # Sample Leads
        leads = [
            Lead(first_name='Alex', last_name='Thompson', email='alex.thompson@newcompany.com', 
                 phone='+1-555-0301', company='NewCompany', status='New', source='Website'),
            Lead(first_name='Lisa', last_name='Garcia', email='lisa.garcia@startup.com', 
                 phone='+1-555-0302', company='Startup', status='Contacted', source='Referral'),
            Lead(first_name='Tom', last_name='Wilson', email='tom.wilson@enterprise.com', 
                 phone='+1-555-0303', company='Enterprise', status='Qualified', source='Social Media'),
            Lead(first_name='Emma', last_name='Davis', email='emma.davis@tech.com', 
                 phone='+1-555-0304', company='TechCompany', status='Unqualified', source='Cold Call'),
            Lead(first_name='Chris', last_name='Miller', email='chris.miller@corp.com', 
                 phone='+1-555-0305', company='CorpInc', status='Converted', source='Email Campaign')
        ]
        db.session.add_all(leads)
        db.session.commit()
        print(f"✅ Added {len(leads)} sample leads")
        
        # Sample Custom Object
        custom_object = CustomObject(
            name='Product',
            label='Product',
            description='Product catalog for tracking inventory and sales',
            fields=json.dumps([
                {'name': 'name', 'type': 'text', 'label': 'Product Name'},
                {'name': 'sku', 'type': 'text', 'label': 'SKU'},
                {'name': 'price', 'type': 'number', 'label': 'Price'},
                {'name': 'category', 'type': 'text', 'label': 'Category'},
                {'name': 'description', 'type': 'textarea', 'label': 'Description'}
            ])
        )
        db.session.add(custom_object)
        db.session.commit()
        print("✅ Created sample custom object (Product)")
        
        # Sample Custom Records
        custom_records = [
            CustomRecord(
                object_id=custom_object.id,
                data=json.dumps({
                    'name': 'Premium Software License',
                    'sku': 'PSL-001',
                    'price': '999.99',
                    'category': 'Software',
                    'description': 'Annual premium software license with full support'
                })
            ),
            CustomRecord(
                object_id=custom_object.id,
                data=json.dumps({
                    'name': 'Cloud Storage Package',
                    'sku': 'CSP-002',
                    'price': '299.99',
                    'category': 'Cloud Services',
                    'description': '1TB cloud storage with backup and sync'
                })
            ),
            CustomRecord(
                object_id=custom_object.id,
                data=json.dumps({
                    'name': 'Consulting Hours',
                    'sku': 'CH-003',
                    'price': '150.00',
                    'category': 'Services',
                    'description': 'Professional consulting services per hour'
                })
            )
        ]
        db.session.add_all(custom_records)
        db.session.commit()
        print(f"✅ Added {len(custom_records)} sample custom records")
        
        # Create sample permission sets
        print("🛡️ Creating sample permission sets...")
        
        # Sales Team Permission Set
        sales_permission_set = PermissionSet(
            name='Sales Team',
            description='Full access to contacts, accounts, opportunities, and leads for sales team members',
            is_active=True
        )
        db.session.add(sales_permission_set)
        db.session.commit()
        
        # Add permissions to Sales Team set
        sales_permissions = [
            PermissionSetPermission(permission_set_id=sales_permission_set.id, object_type='contact', can_view=True, can_create=True, can_edit=True, can_delete=False),
            PermissionSetPermission(permission_set_id=sales_permission_set.id, object_type='account', can_view=True, can_create=True, can_edit=True, can_delete=False),
            PermissionSetPermission(permission_set_id=sales_permission_set.id, object_type='opportunity', can_view=True, can_create=True, can_edit=True, can_delete=False),
            PermissionSetPermission(permission_set_id=sales_permission_set.id, object_type='lead', can_view=True, can_create=True, can_edit=True, can_delete=False),
            PermissionSetPermission(permission_set_id=sales_permission_set.id, object_type='custom_object', object_id=custom_object.id, can_view=True, can_create=True, can_edit=True, can_delete=False)
        ]
        db.session.add_all(sales_permissions)
        
        # Marketing Team Permission Set
        marketing_permission_set = PermissionSet(
            name='Marketing Team',
            description='Access to leads and contacts for marketing team members',
            is_active=True
        )
        db.session.add(marketing_permission_set)
        db.session.commit()
        
        # Add permissions to Marketing Team set
        marketing_permissions = [
            PermissionSetPermission(permission_set_id=marketing_permission_set.id, object_type='contact', can_view=True, can_create=True, can_edit=False, can_delete=False),
            PermissionSetPermission(permission_set_id=marketing_permission_set.id, object_type='lead', can_view=True, can_create=True, can_edit=True, can_delete=False)
        ]
        db.session.add_all(marketing_permissions)
        
        # Support Team Permission Set
        support_permission_set = PermissionSet(
            name='Support Team',
            description='Read-only access to contacts and accounts for support team',
            is_active=True
        )
        db.session.add(support_permission_set)
        db.session.commit()
        
        # Add permissions to Support Team set
        support_permissions = [
            PermissionSetPermission(permission_set_id=support_permission_set.id, object_type='contact', can_view=True, can_create=False, can_edit=False, can_delete=False),
            PermissionSetPermission(permission_set_id=support_permission_set.id, object_type='account', can_view=True, can_create=False, can_edit=False, can_delete=False)
        ]
        db.session.add_all(support_permissions)
        
        db.session.commit()
        print("✅ Created 3 sample permission sets (Sales Team, Marketing Team, Support Team)")
        
        print("\n🎉 Database initialization completed successfully!")
        print("📊 Sample data includes:")
        print(f"   • {len(contacts)} contacts")
        print(f"   • {len(accounts)} accounts") 
        print(f"   • {len(opportunities)} opportunities")
        print(f"   • {len(leads)} leads")
        print(f"   • 1 custom object with {len(custom_records)} records")
        print("\n👤 Login credentials:")
        print("   Username: admin")
        print("   Password: admin123")

# Initialize database when module is imported
def init_app():
    """Initialize the application and database"""
    with app.app_context():
        try:
            # Check if admin user exists
            admin_exists = User.query.filter_by(username='admin').first()
            if not admin_exists:
                print("🔧 Admin user not found. Initializing database...")
                initialize_database()
            else:
                print("✅ Database already initialized.")
        except Exception as e:
            print(f"⚠️  Database initialization error: {e}")
            print("🔄 Attempting to create tables...")
            try:
                db.create_all()
                initialize_database()
            except Exception as e2:
                print(f"❌ Failed to initialize database: {e2}")

# Initialize when module is imported
init_app()

if __name__ == '__main__':
    print("\n🚀 Starting Simple CRM System...")
    print("📱 Access the application at: http://localhost:5000")
    print("👤 Login credentials: admin / admin123")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(debug=True) 