# -*- coding: utf-8 -*-
def index():
    produtos = db(Produtos).select()
    return dict(produtos=produtos)
    


def show_products():
    grid = SQLFORM.grid(db.produtos.id>0)
    return grid


@auth.requires_login()
def product():
    produtos = db(Produtos).select()
    return dict(produtos=produtos)
    
@auth.requires_login()
def product_registration():
    form = SQLFORM(Produtos)

    if form.process().accepted:
        session.flash = 'Produto Cadastrado'
        redirect(URL('product'))
    elif form.errors:
        response.flash = "Erro"
    else:
        response.flash = "Preencha todos os campos"
    return dict(form=form)



@auth.requires_login()
def product_detail():
    produtos = db(Produtos.id == request.args(0)).select()
    print(produtos)
    return dict(produtos=produtos)


@auth.requires_login()
def product_edit():
    form = SQLFORM(Produtos, request.args(0))
    if form.process().accepted:
        session.flash = "Produto atualizado"

        
    elif form.errors:
        response.flash = "Erros no formulário"
    else:
        if not response.flash:
            response.flash = "Preencha o formulário"
    return dict(form=form)


@auth.requires_login()
def product_manager():
    return dict(produtos=produtos)

@auth.requires_login()
def category():
    categorias = db(Categorias).select()
    return dict(categorias=categorias)


@auth.requires_login()
def category_registration():
    form = SQLFORM(Categorias)
    if form.process().accepted:
        session.flash = 'Nova categoria cadastrada: %s' % form.vars.nome_categoria
        redirect(URL('category'))
    elif form.errors:
        response.flash = "Erro"
    else:
        response.flash = "Preencha todos os campos"
    return dict(form=form)