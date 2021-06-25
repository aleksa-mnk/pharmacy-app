'''
****************************
Библиотеки
****************************
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask import Flask, render_template, url_for, flash, redirect, request
import sys

'''
****************************
Глабальные переменные
****************************
'''

HOST = ['0.0.0.0', '127.0.0.1']
PORT = 5000
mnamedic = {'Синупрет':0.5, 'Валериана':0.14, 'Афлубин':0.6}
mtypedic = {'Таблетки':0.5, 'Капли':1.5}
        
'''
****************************
Консолька
****************************

def dataprint():
    for i in range(len(data)):
        print("{}".format(data.get(i)), flush = True)
'''        
'''
****************************
Decorator Pattern 
****************************
'''

class ItemData: 
    def __init__(self, product, types, quantity, delivery, price):
        self._product  = product
        self._types    = types
        self._quantity = quantity 
        self._delivery = delivery
        self._price    = price
    def info(self):
        return ("Лекарство: {}, Вид: {}, Количество: {}, Доставка: {}, Итого: {} тысяч рублей".format(self._product, self._types, self._quantity, self._delivery, self._price))

class AddItem(ItemData): 
    def __init__(self, wrapped): 
        self._wrapped = wrapped
    def add_item_to_cart(self): 
        print("{}".format(self._wrapped.info()), flush = True)
        return('')
'''
*********
на будущее, может сделаю
*********

class RemoveItem(ItemData): 
    def __init__(self, dummy): 
        self._dummy = dummy
    def delete_item_from_cart(self):
        global data
        global ids
        data.pop()
        return ("Removed, ID: {}".format())
'''

'''
****************************
Facade Pattern 
****************************
'''
class WithDelivery:
    def __init__(self, a, b, c):
        self.mamount = mnamedic.get(str(a))
        self.typeamount = mtypedic.get(str(b)) 
        self.quantityamount = c
    #@staticmethod
    def calculate(self):
        return (self.mamount*self.typeamount*float(self.quantityamount))

class WithoutDelivery:
    def __init__(self, a, b, c):
        self.mamount = mnamedic.get(str(a))
        self.typeamount = mtypedic.get(str(b))
        self.quantityamount = c
    #@staticmethod
    def calculate(self):
        return (self.mamount*self.typeamount*float(self.quantityamount))

class BillingFacade:
    '''Facade'''
    def __init__(self, x, y, z, form): 
        self.mname  = x 
        self.typem = y 
        self.quantm = form.mquantity.data 
        self.wdelivery = WithDelivery(x, y, self.quantm)
        self.wodelivery = WithoutDelivery(x, y, self.quantm)
        self.deliverytype = z
        
    def start(self):
        if(self.deliverytype== "С доставкой"):
            res = self.wdelivery.calculate() 
        elif(self.deliverytype == "Без"):
            res = self.wodelivery.calculate() 
        else:
            res = "null"
        product_instance = ItemData(self.mname, self.typem, self.quantm, self.deliverytype, res)
        additem = AddItem(product_instance)
        addres = additem.add_item_to_cart()
        return(product_instance.info(), addres)

'''
****************************
Form 
****************************
'''
class MAinScreen(FlaskForm):

    mquantity = IntegerField('Количество ')#, validators = [ DataRequired()])
    
    submit = SubmitField('Рассчитать')

'''
****************************
Dropdown 
****************************
'''

def dropdown(field_type):
    if(field_type == "medicine"):
        medicine_name = ['Синупрет', 'Валериана', 'Афлубин']
        return (medicine_name)
    elif(field_type == "type"):
        drug_type = ['Таблетки', 'Капли']
        return (drug_type)
    elif(field_type == "delivery"):
        delivery_type = ['С доставкой', 'Без']
        return (delivery_type)

'''
****************************
Инициализация..
****************************
'''

app = Flask(__name__)#, template_folder='templates')

app.config['SECRET_KEY'] = '35156a360226402e7687c3f27d910c27'

@app.route("/", methods=["GET", "POST"])

@app.route("/main", methods=["GET", "POST"])

def hello():
    form = MAinScreen()

    if form.validate_on_submit():
        calc = BillingFacade(request.form["medicinename"], request.form["drugtype"], request.form["deliverytype"], form)
        click = calc.start()
        print(click, file = sys.stderr, flush=True)
        flash('{}'.format(click),'success')
        
    return render_template('main.html', form=form, mname = dropdown("medicine"), mtype = dropdown("type"), delivery = dropdown("delivery"))

'''
****************************
Конец программы
****************************
Instructions to Follow:
    This website is built in Flask API

    The code has 2 Design Patterns

    The Output of Decorator Pattern can be viewed in Console

    All the best!
****************************
'''

if __name__ == '__main__':

    app.run(host=HOST[1], port=PORT, debug=True, threaded=True)