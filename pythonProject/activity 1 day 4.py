litres = float(input("Enter the number of liters you have: "))


bottle_size_litres = 1.5
num_bottles = litres // bottle_size_litres
remaining_litres = litres % bottle_size_litres

print(f"You can fill {int(num_bottles)} bottles.")
print(f"You will have {remaining_litres:.2f} liters of water remaining.")