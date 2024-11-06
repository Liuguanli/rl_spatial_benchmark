import os

class TreeProperties:
    def __init__(self, **kwargs):
        
        self.Dimension = kwargs.get('Dimension', 0)
        self.FillFactor = kwargs.get('Fill factor', 0)
        self.IndexCapacity = kwargs.get('Index capacity', 0)
        self.LeafCapacity = kwargs.get('Leaf capacity', 0)
        self.TightMbrs = kwargs.get('Tight MBRs', 0)
        self.NearMinimumOverlapFactor = kwargs.get('Near minimum overlap factor', 0)
        self.ReinsertFactor = kwargs.get('Reinsert factor', 0)
        self.SplitDistributionFactor = kwargs.get('Split distribution factor', 0)
        self.Utilization = kwargs.get('Utilization', 0)
        self.Reads = kwargs.get('Reads', 0)
        self.Writes = kwargs.get('Writes', 0)
        self.Hits = kwargs.get('Hits', 0)
        self.Misses = kwargs.get('Misses', 0)
        self.TreeHeight = kwargs.get('Tree height', 0)
        self.NumberOfData = kwargs.get('Number of data', 0)
        self.NumberOfNodes = kwargs.get('Number of nodes', 0)
        self.Splits = kwargs.get('Splits', 0)
        self.Adjustments = kwargs.get('Adjustments', 0)
        self.QueryResults = kwargs.get('Query results', 0)
        self.BufferHits = kwargs.get('Buffer hits', 0)
        self.IndexId = kwargs.get('IndexId', 0)
        self.Status = kwargs.get('Status', 0)
        self.ElapsedTime = kwargs.get('Elapsed Time', 0)
        self.ElapsedBuildTime = kwargs.get('Elapsed Build Time', 0)
        self.ElapsedLearnTime = kwargs.get('Elapsed Learn Time', 0)
        if not self.ElapsedTime:
            # if self.ElapsedBuildTime and self.ElapsedLearnTime:
            self.ElapsedTime = self.ElapsedBuildTime + self.ElapsedLearnTime

        self.KnnQuery = kwargs.get('knn query', 0)
        self.IndexedSpace = kwargs.get('Indexed space', 0)
        self.Operations = kwargs.get('Operations', 0)
        self.IndexIo = kwargs.get('Index I/O', 0)
        self.LeafIo = kwargs.get('Leaf I/O', 0)
        
        self.QueryNum = kwargs.get('Query num', 1000)
        self.QueryMean = kwargs.get('Query mean', 0)
        self.QueryVariance = kwargs.get('Query variance', 0)
        self.QueryStdDev = kwargs.get('Query stdDev', 0)
        self.QueryP50 = kwargs.get('Query p50', kwargs.get('Query P50', 0))
        self.QueryP99 = kwargs.get('Query p99', kwargs.get('Query P50', 0))

        self.QueryPercentage = [kwargs.get(f'Query P{i}', 0) for i in range(1, 100, 1)]

        self.InsertNum = kwargs.get('Insert num', 0)
        self.InsertMean = kwargs.get('Insert mean', 0)
        self.InsertVariance = kwargs.get('Insert variance', 0)
        self.InsertStdDev = kwargs.get('Insert stdDev', 0)
        self.InsertP50 = kwargs.get('Insert p50', 0)
        self.InsertP99 = kwargs.get('Insert p99', 0)

        self.TreeDatSize = kwargs.get('Tree.dat Size', 0)
        self.TreeIdxSize = kwargs.get('Tree.idx Size', 0)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join(f"{key}: {value}" for key, value in attrs.items())
    
def parse_rtree_properties(file_path):
    properties = {}
    
    if not os.path.exists(file_path):
        return TreeProperties(**properties)
    
    with open(file_path, 'r') as file:
        for line in file:
            if ": " in line: 
                key, value = line.strip().split(": ", 1)
                
                if value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit():
                    value = float(value)
                properties[key] = value
    return TreeProperties(**properties)