def getMBRFromList(MBRList):
    minx = min([x[0] for x in MBRList])
    maxx = max([x[1] for x in MBRList])
    miny = min([x[2] for x in MBRList])
    maxy = max([x[3] for x in MBRList])
    return (minx, maxx, miny, maxy)

class rtreeNode:
    def __init__(self, childNodeList, MBR=None, isLeaf=False):
        self.childNodeList = childNodeList
        if MBR == None:
            self.MBR = getMBRFromList([node.MBR for node in childNodeList]) 
        else:
            self.MBR = MBR
        self.isLeaf = isLeaf

