import getDinoBoneData

dinosaurs = []
with open('dinosaurs.txt','r') as f:
    for line in f:
        if not line.isspace():
            dinosaurs.append(line.split()[0].replace('"', ''))

# with open('dinosaurs.txt', 'w') as f:
    # for item in dinosaurs:
        # f.write("%s\n" % item)

# dinosaurs = ['Triceratops']
    # 'Tyrannosaurus',
    # 'Allosaurus',
    # 'Velociraptor',
    # 'Ankylosaurus',
    # 'Stegosaurus',
    # 'Apatosaurus',
    # 'Spinosaurus',
    # 'Iguanodon']

# dinosaurs = ['Eucentrosaurus']
    
getDinoBoneData.getData(dinosaurs)