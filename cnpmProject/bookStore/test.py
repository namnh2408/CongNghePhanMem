from bookStore.models import *
from bookStore.utils import *

print(check_role('khanh', UserRole.customer))

result = Cutomers.query.filter(Cutomers.fullname == 'Khanh').first().dislay()

print(result)
# for i in result:
#     print(i)