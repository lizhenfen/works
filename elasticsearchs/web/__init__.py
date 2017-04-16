import sys
import os
path = os.path.dirname(__file__)
package1 = os.path.join(path,'comm')
package2 = os.path.join(path,'conf')
sys.path.insert(0,path)
sys.path.insert(0,package1)
sys.path.insert(0,package2)
