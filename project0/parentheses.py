# το πρόβλημα αυτό είχε πέσει αυτολεξεί σαν ερώτηση 3 της πρώτης εργασίας του μαθήματος των δομών (αρτιων) το περασμένο εξάμηνο
# εκεί υλοποιήθηκε ο παρακάτω αλγόριθμος:
#
# 1. push to stack until you find a ')'
# 2. stack.pop 3 times, put the stuff in order (last item is the second number) so:
# .. second = stack.pop()
# .. operator = stack.pop()
# .. first = stack.pop()
# 3. combine to a string with parentheses "(%s%s%s)", first, operator, second
# 4. push the string to the stack
# 5. repeat until EOF
# 6. Pop, the popped string is the expression fixed  
# 
# θα χρησιμοποιήσουμε μια λίστα για το stack data structure 
# ωστόσο υπάρχει ένα πρόβλημα λόγω του περιορισμού ότι πρέπει να χρησιμοποιήσουμε μόνο λίστες και όχι strings (βλ παρακάτω)

def complete_parentheses(expression):
    stack = []
    for char in expression:
        if char == ')':
            second = stack.pop()  # Right operand
            operator = stack.pop()  # Operator
            first = stack.pop()  # Left operand
            # Combine into a fully parenthesized expression list
            combine = ["(", first, operator, second, ")"]
            stack.append(combine)
        else:
            stack.append(char)
    return stack.pop()

# στο τελος, θα έχουμε μια λίστα κάπως ετσι: 
# ['(', ['(', '1', '+', '2', ')'], '*', ['(', ['(', '3', '–', '4', ')'], '*', ['(', '5', '–', '6', ')'], ')'], ')']
# προφανως μπορούμε να δούμε ότι σε αυτήν την λίστα υπάρχει (καπως) η εκφραση που θέλουμε, αλλά δεν είναι εύκολο να την τυπώσουμε
# διότι πρόκειται για μια μπλεγμένη λίστα από λίστες (από λίστες από λίστες...) με άγνωστο αριθμό "βάθους λιστών"
# αυτό γίνεται διότι το first και το second στην συνάρτηση complete_parentheses πιθανόν να ειναι λίστες από την προηγούμενη φορά που συναντήσαμε ')'
# γιαυτό χρειαζομαστε μια συνάρτηση για να κάνουμε flatten λίστα οποιουδήποτε βάθους από λίστες σε string

def flatten_list(expression):
    if not isinstance(expression, list): # base case: αν δεν είναι λίστα, επέστρεψε το σαν string
        return str(expression)
    return ' '.join([flatten_list(x) for x in expression]) # αλλιώς, κανε recursively join τα στοιχεία της λίστας μεταξύ τους
    #στο τελος θα έχουμε ένα string που θα αποτελείται από ένα ένα τα στοιχεία της αρχικής λίστας, αλλα και κάθε λίστας μέσα σε αυτήν

def main():
    # η παράσταση πρέπει να δίνεται με κενά ακριβώς όπως στην εκφώνηση
    expression = input("Enter an expression (as a space-separated list): ").split() 
    result = list(complete_parentheses(expression))
    print((flatten_list(result)))
    

if __name__ == "__main__":
    main()

