reserved_words = ['πρόγραμμα', 'δήλωση', 'εάν', 'τότε', 'αλλιώς', 'εάν_τέλος', 'επανάλαβε', 'μέχρι', 'όσο', 'όσο_τέλος',
                  'για', 'έως', 'με_βήμα', 'για_τέλος', 'διάβασε', 'γράψε', 'συνάρτηση', 'διαδικασία', 'διαπροσωπεία',
                  'είσοδος', 'έξοδος', 'αρχή_συνάρτησης', 'τέλος_συνάρτησης', 'αρχή_διαδικασίας', 'τέλος_διαδικασίας',
                  'αρχή_προγράμματος', 'τέλος_προγράμματος', 'ή', 'και', 'εκτέλεσε']

quadList = []
listOfVariables = []
T_i_counter = 0
function_name = ""
counter_nextquad = 0
nesting = 0
scopeList = []
deletedScopes = []
functions = []
declaredVariables = []
functionReturn = False
for_identifiers = []
programName = ""
parCounter = 0
varListCaller = ""