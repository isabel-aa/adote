from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
# Create your views here.

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')
    #  verificar se o usuário antes de acessar a pagina de cadastro está já logado, SE ele ja estiver logado eu nao vou deixar ele acessar a pagina de cadastro
    if request.method == "GET":
        return render(request, 'cadastro.html') #se minha requisição for GET eu mostro meu html cadastro
    elif request.method == "POST": #se minha requisição for POST eu quero pegar os dados que foram enviados e cadastrar uma nova pessoa depois disso o python vai processar os dados para salvar no banco de dados
        nome = request.POST.get('nome') #vou criar uma variável python para receber esses dados + o METODO QUE USEI eexatamente a informação que eu quero  #da minha requsição do METODO POST. PEGUE (GET) A informação que tenha o name la dentro do meu html
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

#para não deixar o campo nome vazio ou com espaço vazios não permite o usuario se cadastrar utilizando o if len e o OR como se o len ....
        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos') # essa é a mensagem que vai aparecer na tela
            return render(request, 'cadastro.html') #faz o usuario voltar para a pagina de cadastro
        
        if senha != confirmar_senha: # se a senha for diferente de confirmar senha volta para a pagina
            messages.add_message(request, constants.ERROR, 'Digite duas senhas iguais')
            return render(request, 'cadastro.html')
      
        try: #significa tentar isso
            user = User.objects.create_user( #quando eu fizer isso ele vai salvar o usuario no banco de dados pra mim
                username=nome,
                email=email,
                password=senha
            )
            messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso')
            return render(request, 'cadastro.html')
        except: # se nao der com o que usamos no TRY usamos o except para 
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return render(request, 'cadastro.html')

#OBSERVAÇÃO APÓS COLOCAR A MENSAGEM TEM QUE APARECER DENTRO DO NOSSO HTML 

#preciso do form e input ter os nomes pq através desses nomes que vamos saber o que é op que la no backend 
#e é através deles que vamos receber esses dados la no nosso backend, então
#nossos dados vai sair do frontend fazer uma requisição via requisição via POST e no backend vamos tratar esses dados qnd o usuario clicar no botão SALVAR

def logar(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')
    #  verificar se o usuário antes de acessar a pagina de cadastro está já logado, SE ele ja estiver logado eu nao vou deixar ele acessar a pagina de cadastro
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(username=nome,
                            password=senha) #django verifica (autenticando pra mim se tem algum usuario com esse nome e senha SE NAO ENCONTRAR RETORNA 'NONE'

        if user is not None:
            login(request, user)
            return redirect('/divulgar/novo_pet')

        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos')
            return render(request, 'login.html')
        #return HttpResponse(f'{nome}, {senha}') #conferindo se os dados estão realmente sendo gerados corretamente

def sair(request):
    logout(request)
    return redirect('/auth/login')

   # if request.user.is_authenticated:
   #     return redirect('/divulgar/novo_pet')
