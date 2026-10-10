from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
import base64

# -------------------------------
# KEY GENERATION
# -------------------------------
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()

# -------------------------------
# SAVE KEYS
# -------------------------------
def save_private_key(private_key, filename):
    with open(filename, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

def save_public_key(public_key, filename):
    with open(filename, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

# -------------------------------
# LOAD KEYS
# -------------------------------
def load_private_key(filename):
    with open(filename, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(filename):
    with open(filename, "rb") as f:
        return serialization.load_pem_public_key(f.read())

# -------------------------------
# ENCRYPT MESSAGE
# -------------------------------
def encrypt_message(message, public_key):
    sym_key = Fernet.generate_key()
    cipher = Fernet(sym_key)

    encrypted_msg = cipher.encrypt(message.encode())

    encrypted_key = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_msg, encrypted_key

# -------------------------------
# DECRYPT MESSAGE
# -------------------------------
def decrypt_message(enc_msg, enc_key, private_key):
    sym_key = private_key.decrypt(
        enc_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher = Fernet(sym_key)
    return cipher.decrypt(enc_msg).decode()

# -------------------------------
# SIGN MESSAGE
# -------------------------------
def sign_message(message, private_key):
    return private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

# -------------------------------
# VERIFY SIGNATURE
# -------------------------------
def verify_signature(message, signature, public_key):
    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

# -------------------------------
# SEND EMAIL
# -------------------------------
def send_email(sender_email, app_password, receiver_email, enc_msg, enc_key, signature):
    enc_msg_b64 = base64.b64encode(enc_msg).decode()
    enc_key_b64 = base64.b64encode(enc_key).decode()
    sig_b64 = base64.b64encode(signature).decode()

    full_message = f"""
ENCRYPTED_MESSAGE:
{enc_msg_b64}

ENCRYPTED_KEY:
{enc_key_b64}

SIGNATURE:
{sig_b64}
"""

    msg = MIMEText(full_message)
    msg['Subject'] = " Secure Email (PGP)"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    print("\n📧 Email Sent Successfully!")

# -------------------------------
# RECEIVE & DECRYPT
# -------------------------------
def receive_and_decrypt(private_key_file, sender_public, enc_msg_b64, enc_key_b64, sig_b64):
    private_key = load_private_key(private_key_file)

    enc_msg = base64.b64decode(enc_msg_b64)
    enc_key = base64.b64decode(enc_key_b64)
    signature = base64.b64decode(sig_b64)

    decrypted = decrypt_message(enc_msg, enc_key, private_key)
    valid = verify_signature(decrypted, signature, sender_public)

    print("\n📥 Decrypted Message:", decrypted)
    print("✍️ Signature:", "Valid ✅" if valid else "Invalid ❌")

# -------------------------------
# MAIN MENU
# -------------------------------
if __name__ == "__main__":
    print("🔐 Advanced Secure Email System (PGP)\n")

    print("1. Send Secure Email")
    print("2. Decrypt Received Email")

    choice = input("Enter choice: ")

    # ---------------- SEND ----------------
    if choice == "1":
        sender_private, sender_public = generate_keys()
        receiver_private, receiver_public = generate_keys()

        # SAVE KEYS (IMPORTANT)
        save_private_key(receiver_private, "receiver_private.pem")
        save_public_key(receiver_public, "receiver_public.pem")
        save_public_key(sender_public, "sender_public.pem")

        sender_email = input("Enter your Gmail: ")
        app_password = input("Enter App Password: ")
        receiver_email = input("Enter Receiver Email: ")
        message = input("Enter Message: ")

        enc_msg, enc_key = encrypt_message(message, receiver_public)
        signature = sign_message(message, sender_private)

        send_email(sender_email, app_password, receiver_email, enc_msg, enc_key, signature)

        print("\n✅ Keys saved successfully!")

    # ---------------- RECEIVE ----------------
    elif choice == "2":
        print("\nPaste from email:")

        enc_msg_b64 = input("Encrypted Message: ")
        enc_key_b64 = input("Encrypted Key: ")
        sig_b64 = input("Signature: ")

        # LOAD CORRECT SENDER PUBLIC KEY
        sender_public = load_public_key("sender_public.pem")

        receive_and_decrypt("receiver_private.pem", sender_public, enc_msg_b64, enc_key_b64, sig_b64)

    else:
        print("Invalid choice")
