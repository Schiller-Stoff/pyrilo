import fasttext
import fasttext.util

ft = fasttext.load_model('./models/cc.de.300.bin')
print(ft.get_dimension())
fasttext.util.reduce_model(ft, 20)
print(ft.get_dimension())

ft.save_model('./models/cc.de.20.bin')
