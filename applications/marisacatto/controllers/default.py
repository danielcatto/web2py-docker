# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ---


def index():
    import random

    form = SQLFORM.factory(
        Field('valor')
        )

    if form.process().accepted:
        valor_informado =  form.vars.valor
    else:
        valor_informado = 1
    
    valor_area_str = valor_informado #
    valor_area = int(valor_area_str)
    resultado_perimentro = valor_area * 4
    resultado_area = valor_area * valor_area
    resultado = valor_area, resultado_perimentro , resultado_area
    
   

    k = random.randint(0, 100)
    if k % 4 == 0:
        a = str(k), ' is divisible by 4'
    elif k%2 == 0:
        a = str(k), ' is even'
    else:
        a = str(k), ' is odd'

    res = 700 / 4


    if not session.counter:
        session.counter = 1
    else:
        session.counter += 1
    

    return dict(counter=session.counter, carrinho=session.carrinho, a=a, res=res, resultado=resultado, form=form)


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def login():
    return dict(login=login)


###teste pessoa insert
def pessoa():
    form = SQLFORM(Pessoa)
    if form.process().accepted:
        session.flash = 'registered ok', form.vars.id
        redirect(URL('index'))
    elif form.errors:
        response.flash = "Erro"
    else:
        response.flash = "Fill in all fields"
    return dict(form=form)

###########################################
############## VENDAS #####################
###########################################
@auth.requires_login()
def vendas():
    return dict(vendas=vendas)

#vendas
@auth.requires_login()
def itens_compras():
    pass

#@auth.requires_login()
def vender():
    cart=tuple()
    if not session.carrinho:
        session.carrinho = list()
        session.sub = 0
    
    form = SQLFORM.factory(
        Field('codigo', requires=IS_NOT_EMPTY(), label='Código'),
        Field('quantidade',requires=IS_NOT_EMPTY())
        )
        

    if form.process().accepted:
        produtos = db(Produtos.id == form.vars.codigo).select()
        if produtos:
            qtd = form.vars.quantidade
            total =  float(produtos[0]['valor']) * float(qtd)
            session.sub += total
            cart = (produtos, qtd, total)
            session.carrinho.append(cart)
        else:
            print('#################\n\n\n\n\n\n\nferrou')
    else:
        produtos = 'vazio'
    print(type(produtos))
    return dict(form=form)

def show_cart():
    if not session.cart:
        session.cart = []
    try:
        cart = session.cart
    except:
        cart = ''

    return dict(cart=cart)

def delete_cart():
    session.cart = ''
    redirect(URL('products', 'product'))
 

def cart():
    if not session.cart:
        session.cart = []
    try:
        product_query = db(Produtos.id == request.args(0, cast=int)).select()
        
        #print('testes ini', product_query, 'teste')
        quantidade = 1

        if product_query:
                for i in range(len(product_query)):
                    sub_total = float(product_query[i]['valor']) * float(quantidade)

                    product = (product_query[i]['id'], product_query[i]['nome'], product_query[i]['valor'], quantidade, sub_total)
                    session.cart.append(product)
                    redirect(URL('default', 'show_cart'))
    except:
        cart=session.cart
    return dict(cart=session.cart)


################################

def cart_form():
    if not session.cliente:
        session.cliente = ''
        session.cart = []
        session.sub = 0
    query = ''
    product_query=''
    product = tuple()
    
    form = SQLFORM.factory(
        Field('codigo', requires=IS_NOT_EMPTY(), label='Código')
        )
    if form.process(formname='form').accepted:
            query = db(Clientes.id == form.vars.codigo).select()
            if query:
                session.cliente = (query[0]['id'],query[0]['nome'])
                print('session.cliente[0]', session.cliente[0])

    form_product = SQLFORM.factory(
        Field('product_id', requires=IS_NOT_EMPTY(), label='Código produto'),
        Field('quantidade', requires=IS_NOT_EMPTY(), label='Quantidade')
        )

    if form_product.process(formname='form_product').accepted:
        product_query = db(Produtos.id == form_product.vars.product_id).select()
        quantidade = form_product.vars.quantidade
        if product_query:
            for i in range(len(product_query)):
                sub_total = float(product_query[i]['valor']) * float(quantidade)
                session.sub = session.sub + sub_total
                product = (product_query[i]['id'], product_query[i]['nome'], product_query[i]['valor'], quantidade, sub_total)
                session.cart.append(product)                 
    return dict(form=form, form_product=form_product, cart=session.cart, cliente=session.cliente) 


def finalizar():
    cliente_id = session.cliente[0]
    cliente_nome = session.cliente[1]

    cart = session.cart
    
    #for i in range(len(cart)):
        #print(cart[i][0])

    #db.vendas.insert(cliente_id=cliente_id, nome=cliente_nome)

    print('retorno insert ', db.vendas.insert)
    #redirect(URL('default', 'delete_cart'))
    return dict(finalizar=finalizar)

def delete_cart():
    session.cliente = None
    session.cart = None
    return dict(delete_cart=delete_cart)

#teste com data 
def contando_data():

    ano= 2020       #formato AAA
    mes=  5       #usar numeros
    dia= 22
    import datetime

    datapadrao = datetime.date(ano, mes, dia)
    hoje = datetime.date.today()

    if datapadrao > hoje:
        delta = datapadrao - hoje

    elif datapadrao <= hoje:
        delta = hoje - datapadrao

    resultado_delta = delta.days

    return dict(resultado_delta=resultado_delta, ano=ano, mes=mes, dia=dia)


def display_form():
    form=FORM('Your name:', INPUT(_name='name'), INPUT(_type='submit'))
    return dict(form=form)   


