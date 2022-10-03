from cmath import log
from logging import root
import xml.etree.ElementTree as gfg
from product import Product

def create_gomba_xml(data: Product, parameter_counter_id, sizes_ids):
    parser = gfg.XMLParser(encoding="utf-8")
    tree = gfg.parse('products.xml', parser=parser)
    root = tree.getroot()
    product = gfg.Element('product')
    root.append(product)
    gfg.SubElement(product,'code').text = data.code
    gfg.SubElement(product,'title').text = data.title
    gfg.SubElement(product,'description').text = data.description
    category = gfg.SubElement(product,'category')
    category.text = data.categoryName
    category.set('id',str(data.categoryId))
    gfg.SubElement(product,'brand').text = data.brand
    photos = gfg.SubElement(product,'photos')
    
    for image in data.images:
        gfg.SubElement(photos,'photo').text = image
        
    gfg.SubElement(product,'price').text = data.price
    gfg.SubElement(product,'qtty').text = '10'
    gfg.SubElement(product,'availability').text = '10'
    gfg.SubElement(product,'trackInventory').text = '0'
    gfg.SubElement(product,'isPromo').text = '0'
    gfg.SubElement(product,'isNew').text = '0'
    gfg.SubElement(product,'hidden').text = '0'
    gfg.SubElement(product,'url').text = ''
    gfg.SubElement(product,'pageTitle').text = data.title
    gfg.SubElement(product,'pageDescr').text = data.description
    parameters= gfg.SubElement(product,'parameters')
    parameter = gfg.SubElement(parameters,'parameter')
    parameter.set('id',str(parameter_counter_id))
    parameter.set('orderId',"10000")
    parameter.set('typeId','')
    parameter.set('hasVariants',"1")
    parameter.set('required',"")
    
    gfg.SubElement(parameter,'name').text = 'Размер'
    parameter_options = gfg.SubElement(parameter,'options')
    
    for i in range(len(data.sizes)):
        size = data.sizes[i]
        option = gfg.SubElement(parameter_options,'option')
        option.text = size
        option.set("id", str(sizes_ids[i]))
        option.set("price", "0.00")
        
    variants = gfg.SubElement(product,'variants')
    
    for i in range(len(data.sizes)):
        variant = gfg.SubElement(variants,'variant')
        variant.set("sku", f"1-*{str(parameter_counter_id)}-{sizes_ids[i]}*")
        variant.set("code", "")
        variant.set("barcode", "")
        variant.set("price", data.price.replace(",","."))
        variant.set("qtty","0")
        variant.set("trackInventory","0")
        variant.set("inventoryPrice","0")
        variant.set("orderId","10000")
        
    
        
        
    
    tree = gfg.ElementTree(root)
    # print(data)
    with open("products.xml", 'a',encoding='utf8') as file:
        tree.write("products.xml",encoding='utf8')

    
    
    