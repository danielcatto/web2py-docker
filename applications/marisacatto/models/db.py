# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

#db = DAL('mysql://root:root@192.168.10.162/banco_web2py')
if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    #db = DAL('mysql://root:root@192.168.10.50/db')
    #db = DAL( "postgres://admin:admin1234@postgresql_database:5432/db")
    #db = DAL('postgres://admin:admin1234@postgresql_database/db')

    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets There
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configure.get('heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)


Clientes = db.define_table('clientes',
                                Field('nome','string'),
                                Field('cpf', 'integer'),
                                Field('cep', 'integer'),
                                Field('logradouro', 'string'),
                                Field('num','string'),
                                Field('bairro', 'string'),
                                Field('cidade', 'string'),
                                Field('uf', 'string'),
                                Field('data_cadastro', 'date'),
                                #primarykey=['id']
                                )

#Clientes.num.requires=IS_NOT_EMPTY()
Clientes.data_cadastro.requires=IS_EMPTY_OR(IS_DATE(format='%d/%b/%Y'))
Clientes.nome.requires=IS_NOT_EMPTY()
Clientes.cpf.requires=IS_NOT_EMPTY()
Clientes.cep.requires=IS_NOT_EMPTY()
Clientes.logradouro.requires=IS_NOT_EMPTY()
Clientes.bairro.requires=IS_NOT_EMPTY()
Clientes.cidade.requires=IS_NOT_EMPTY()
Clientes.uf.requires=IS_NOT_EMPTY()




#Tabela de Categorias de Produtos
Categorias = db.define_table('categorias', Field('nome_categoria', 'string'))
Categorias.nome_categoria.requires=IS_NOT_EMPTY()


#TABELA DE PRODUTOS
Produtos = db.define_table('produtos',
                            Field('nome', 'string'),
                            Field('valor', 'float'),
                            Field('quantidade', 'integer'),                        
                            Field('imagemdoproduto','upload',label='Imagem do produto'),
                            Field('data_cadastro', 'datetime', default=request.now),                           
                            Field('categoria', 'reference categorias')
                            )
                            
Produtos.nome.requires=IS_NOT_EMPTY()
Produtos.valor.requires=IS_NOT_EMPTY()
Produtos.quantidade.requires=IS_NOT_EMPTY()
Produtos.data_cadastro.requires = IS_DATETIME(format='%d/%m/%Y')
Produtos.data_cadastro.requires=IS_NOT_EMPTY()



Itens = db.define_table('itens',
			    Field('pedido', 'integer'),
			    Field('codigo_produto', 'integer'),
			    Field('quantidade', 'float'),
			    Field('valor', 'float'),
			    Field('sub_total', 'float')
			     )


Venda =  db.define_table('vendas',
                            
                            Field('cliente_id','integer'),
                            Field('nome', 'string'),                     
                            Field('total_compra', 'float'),
                            Field('forma_pagamento', 'string'),
                            Field('status', 'boolean')
                            )
