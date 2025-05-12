import random
import string

def generate_password():
    # Get user inputs
    while True:
        try:
            length = int(input("Enter desired password length: "))
            if length <= 0:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    strength = input("Enter password strength (weak/medium/strong): ").lower()
    while strength not in ['weak', 'medium', 'strong']:
        print("Invalid strength choice. Please choose weak, medium, or strong.")
        strength = input("Enter password strength (weak/medium/strong): ").lower()

    personalize = input("Do you want to personalize the password with your name and age? (yes/no): ").lower()
    while personalize not in ['yes', 'no']:
        print("Please answer yes or no.")
        personalize = input("Do you want to personalize the password with your name and age? (yes/no): ").lower()

    name, age = '', ''
    if personalize == 'yes':
        name = input("Enter your name: ").strip()
        while True:
            age = input("Enter your age: ").strip()
            if age.isdigit() and int(age) > 0:
                break
            print("Please enter a valid positive number for age.")

    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # Determine character set and requirements based on strength
    strength_params = {
        'weak': {'charset': lowercase + digits, 'required': [lowercase, digits]},
        'medium': {'charset': lowercase + uppercase + digits, 'required': [lowercase, uppercase, digits]},
        'strong': {'charset': lowercase + uppercase + digits + symbols, 'required': [lowercase, uppercase, digits, symbols]}
    }

    params = strength_params[strength]
    charset = params['charset']
    required_sets = params['required']

    if personalize == 'yes':
        # Personalized password generation
        personal_chars = list(name + age)
        required_chars = []

        # Check for missing required character types
        for s in required_sets:
            if not any(c in s for c in personal_chars):
                required_chars.append(random.choice(s))

        # Calculate minimum required length
        min_length = len(personal_chars) + len(required_chars)
        if length < min_length:
            print(f"Error: Password length must be at least {min_length} to include personal information and meet security requirements.")
            return

        # Build password components
        combined = personal_chars + required_chars
        remaining_length = length - len(combined)

        # Add random characters if needed
        if remaining_length > 0:
            combined += random.choices(charset, k=remaining_length)

        # Shuffle and truncate to desired length
        random.shuffle(combined)
        password = ''.join(combined[:length])
    else:
        # Generate required characters
        required_chars = [random.choice(s) for s in required_sets]
        if length < len(required_chars):
            print(f"Error: Password length must be at least {len(required_chars)} for selected strength.")
            return

        # Generate remaining characters
        remaining = length - len(required_chars)
        password_chars = required_chars + random.choices(charset, k=remaining)
        random.shuffle(password_chars)
        password = ''.join(password_chars)

    # Final validation
    if personalize == 'yes':
        # Verify all required character types are present
        for s in required_sets:
            if not any(c in s for c in password):
                print("Warning: Generated password doesn't meet strength requirements. Please try a longer password.")
                return

    print("\nGenerated Password:", password)
    print("Password Length:", len(password))

if __name__ == "__main__":
    generate_password()