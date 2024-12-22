# Coinbase_Wallet
# Coinbase Wallet Django Project

A Django-based project that implements a persistent wallet on Base testnet with automated funding capabilities using the Coinbase Developer Platform.

## Project Overview

This project creates and manages a persistent wallet on Base testnet with the following features:
- Wallet creation and persistence across multiple script executions
- Automated funding using Base testnet faucet
- Wallet information display including public address and ETH balance
- Integration with Coinbase Developer Platform using CDP SDK

## Prerequisites

- Python 3.8+
- Django
- Coinbase Developer Platform Account
- Base Testnet access

## Installation

1. Clone the repository
```python
git clone [your-repository-url]
cd coinbase_wallet
```

2. Create and activate a virtual environment
```python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages
```python
pip install Django
pip install cdp-sdk
pip install python-dotenv
```

## Project Structure
```
coinbase_wallet/
├── .env                    # Environment variables (not in git)
├── manage.py
├── wallet_data.json        # Stored wallet data
├── my_seed.json           # Encrypted wallet seeds
├── coinbase_wallet/       # Project directory
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── wallet/               # App directory
    ├── __init__.py
    ├── views.py
    ├── urls.py
    └── models.py
```

## Configuration

1. Create a `.env` file in the root directory with your API credentials:
```
API_KEY_NAME=your_api_key_name
API_KEY_PRIVATE_KEY=your_api_key_private_key
```

2. Update `settings.py` to load environment variables:
```python
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add 'wallet' to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'wallet',
]
```

3. Configure project URLs (`coinbase_wallet/urls.py`):
```python
from django.urls import path, include

urlpatterns = [
    path('', include('wallet.urls')),
]
```

4. Configure app URLs (`wallet/urls.py`):
```python
from django.urls import path
from .views import configure_cdp, create_wallet

urlpatterns = [
    path('configure_cdp/', configure_cdp, name='configure_cdp'),
    path('create_wallet/', create_wallet, name='create_wallet'),
]
```

## API Endpoints

### 1. Configure CDP
- **Endpoint**: `/configure_cdp/`
- **Method**: GET
- **Description**: Configures the CDP SDK with your API credentials
- **Response**: Success or error message with appropriate HTTP status code

### 2. Create Wallet
- **Endpoint**: `/create_wallet/`
- **Method**: GET
- **Description**: Creates a new wallet on Base Sepolia testnet with automatic funding
- **Features**:
  - Creates a new wallet with multiple addresses
  - Automatically funds the wallet using Base testnet faucet
  - Stores wallet data securely
  - Encrypts and saves wallet seed
- **Response Example**:
```json
{
    "message": "Wallet created successfully",
    "wallet_id": "8117836e-a4bf-45f2-b215-1daba31e933b",
    "default_address": "0x...",
    "addresses": ["0x...", "0x..."],
    "Wallet_status": "Fund transferred successfully into the wallet at https://sepolia.basescan.org/tx/0x...",
    "wallet_balance": "Balance of the wallet is {...}"
}
```

### Data Storage
The project implements two types of persistent storage:

1. **Wallet Data Storage** (`wallet_data.json`):
- Stores wallet IDs, seeds, and network information
- Format:
```json
{
  "wallet_id": {
    "wallet_id": "uuid",
    "seed": "wallet_seed",
    "network_id": "base-sepolia"
  }
}
```

2. **Encrypted Seed Storage** (`my_seed.json`):
- Stores encrypted wallet seeds with authentication tags
- Encrypted using CDP secret API key
- Format:
```json
{
  "wallet_id": {
    "seed": "encrypted_seed",
    "encrypted": true,
    "auth_tag": "auth_tag",
    "iv": "initialization_vector",
    "network_id": "base-sepolia"
  }
  
}
```

## Getting Started

1. Set up your Coinbase Developer Platform account and generate API keys.

2. Clone the repository and install dependencies as described in the Installation section.

3. Create and configure your `.env` file with your API credentials.

4. Run migrations:
```python
python manage.py migrate
```

5. Start the development server:
```python
python manage.py runserver
```

6. Test the endpoints:
```python
# Configure CDP
curl http://localhost:8000/configure_cdp/

# Create a new wallet
curl http://localhost:8000/create_wallet/
```

