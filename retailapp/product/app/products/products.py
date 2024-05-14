from flask import Flask, Blueprint, jsonify, request, abort ,redirect, url_for
from app.schema.models import Product

products_bp = Blueprint("products_bp", __name__)

@products_bp.route("/getproducts")
def getProducts():
        productlist = request.args.get("productlist")
        product = Product()
        try:
                products = product.getProducts(productlist)
        except Exception as e:
                try:
                        products = product.getProducts(productlist)
                except Exception as e:
                        print ("EXCEPTION: {}".format(e))
                        abort(500)
        return jsonify({'title': 'Products List', 'products': products})

@products_bp.route("/popularitems")
def popular_items():
        top = request.args.get("top", 5) and int(request.args.get("top", 5)) or None
        interval = request.args.get("interval", 5) and int(request.args.get("interval", 5)) or None
        product = Product()
        product_items = product.popular_items(top, interval)
        return jsonify({'title': 'Popular Products', 'product_items': product_items})

@products_bp.route("/view")
def view():
	id = request.args.get("id") and int(request.args.get("id")) or None
	product = Product()
	try:
		return get_product(product, id)
	except Exception as e:
		try:
			return get_product(product, id)
		except Exception as e:
			print ("EXCEPTION: {}".format(e))
			abort(500)

@products_bp.route("/whereami")
def whereami():
	product = Product()
	try:
		return jsonify(product.whereami())
	except Exception as e:
		try:
			return jsonify(product.whereami())
		except Exception as e:
			print ("EXCEPTION: {}".format(e))
			abort(500)

@products_bp.route("/<product>")
def main(product):
	product_name = product
	product = Product(product)
	product_items = product.return_items()
	id = request.args.get("id") and int(request.args.get("id")) or None

	if product_items is None:
		abort(404)
	else:
		if id:
			product_items = [dict(p) for p in product_items if p['id'] == id]
		else:
			product_items= [dict(p) for p in product_items]
		return jsonify({'title': product_name, 'product_items': product_items})
	
@products_bp.route("/<product>/<product_item>")
def view_product(product, product_item):
	product = Product(product)
	product_items = product.return_items()
	product_items = [dict(p) for p in product.return_items()] 
	product_name = [p for p in product_items if p['name'].lower() == product_item.lower()]
	if len(product_name) == 0:
		abort(404)
	else:
		return jsonify({'title': product_item, 'product_items': product_items})

def get_product(product, id):
	product_items = product.show_all_items_new(id)
	product_items = [dict(p) for p in product_items]
	print ( jsonify({'title': 'Product View', 'product_items': product_items}) )
	return jsonify({'title': 'Product View', 'product_items': product_items})
	
@products_bp.route("/<category>/add")
def addProduct():
        product = request.args.get("product")
        print (product)
        product = Product()
        try:
                result = product.addProduct(category, product)
        except Exception as e:
                try:
                        result = product.addProduct(category, product)
                except Exception as e:
                        print ("EXCEPTION: {}".format(e))
                        abort(500)
        return jsonify({'title': 'Product Add', 'category': category, 'product': result})
