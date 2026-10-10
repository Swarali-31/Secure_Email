# Secure Email Communication Using Hybrid Encryption

**Information and Network Security — Case Study on PGP Implementation**

## 1. Project Overview

This project demonstrates secure email communication using a hybrid encryption approach inspired by Pretty Good Privacy (PGP). It combines symmetric encryption, asymmetric encryption, and digital signatures to protect email messages during transmission.

The system is implemented in Python and runs on Kali Linux. It demonstrates how encrypted messages can be sent through SMTP and decrypted and verified by the intended recipient.

## 2. Objectives

- Protect email confidentiality using hybrid encryption.
- Use AES-based symmetric encryption for message encryption.
- Use RSA public-key cryptography for secure session-key exchange.
- Generate and verify digital signatures to detect message tampering and support sender authentication.
- Demonstrate secure and insecure email communication.

## 3. Technologies Used

- **Programming Language:** Python 3
- **Operating System:** Kali Linux
- **Cryptographic Library:** `cryptography`
- **Encryption:** Fernet (symmetric encryption) and RSA (asymmetric encryption)
- **Digital Signatures:** RSA with PSS padding and SHA-256
- **Email Protocol:** SMTP
- **Python Standard Libraries:** `smtplib`, `email`, and `base64`, as used by the implementation

## 4. System Workflow

1. Generate public and private key pairs for the sender and recipient.
2. Generate a symmetric session key.
3. Encrypt the email message using symmetric encryption.
4. Encrypt the session key using the recipient's public key.
5. Sign the original message using the sender's private key.
6. Transmit the encrypted message, encrypted session key, and digital signature through SMTP.
7. At the receiving end, decrypt the session key using the recipient's private key.
8. Decrypt the original message and verify the digital signature using the sender's public key.

## 5. Prerequisites

- Kali Linux or a compatible Linux distribution
- Python 3
- pip for Python package installation
- Internet connectivity for email transmission
- An email account configured for SMTP access
- An app password or other supported SMTP authentication method

## 6. Installation and Setup

Open a terminal and navigate to the project directory.

```bash
cd /path/to/email_project
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required cryptographic library:

```bash
python -m pip install cryptography
```

If a `requirements.txt` file is included, install the listed dependencies instead:

```bash
python -m pip install -r requirements.txt
```

## 7. How to Execute the Project

Run the main Python script from the project directory:

```bash
python3 secure_email.py
```

Replace `secure_email.py` with the actual name of the main Python file if it differs.

The program presents a menu with options to:

1. Send a secure email.
2. Decrypt a received email.

Follow the on-screen prompts. To send an email, provide the required sender and recipient details, message content, and SMTP credentials. To decrypt a received message, provide the encrypted message, encrypted session key, and signature as requested by the program.

## 8. Expected Output

When sending a secure email, the program should encrypt the message, generate the required cryptographic data, and transmit the email through SMTP.

When receiving a message, the program should decrypt the original content and report whether the digital signature is valid.

The encrypted email contains encoded encrypted data rather than readable original message content.

## 9. Security Considerations

- Never upload private keys, email passwords, app passwords, or other secrets to a public repository.
- Keep private keys protected and accessible only to their intended owners.
- Use the recipient's public key for session-key encryption and the sender's private key for signing.
- Verify digital signatures before trusting received messages.
- SMTP configuration may differ depending on the email provider.

## 10. Project Files

The repository contains the Python source code, required configuration and dependency files, and supporting resources needed to run the project.

## 11. GitHub Repository

**Repository URL:** Add your GitHub repository URL here.

## 12. Conclusion

This project demonstrates the practical application of hybrid cryptography in email communication. It illustrates how symmetric encryption, RSA-based key exchange, and digital signatures can be combined to provide confidentiality and message-integrity verification.

