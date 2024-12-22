import os
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from cdp import *
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
import json


@require_http_methods(["GET"])
def configure_cdp(request):
    api_key_name = os.environ.get('api_key_name')
    api_key_private_key = os.environ.get('api_key_private_key')
    
    if not api_key_name or not api_key_private_key:
        return JsonResponse({
            "error": "Missing API credentials. Please set api_key_name and api_key_private_key environment variables."
        }, status=400)
    
    try:
        Cdp.configure(api_key_name, api_key_private_key)
        return JsonResponse({"message": "CDP SDK has been successfully configured with CDP API key."})
    except Exception as e:
        return JsonResponse({"error": f"Failed to configure CDP: {str(e)}"}, status=500)

@require_http_methods(["GET"])
def create_wallet(request):
    try:
        # Create wallet - explicitly specify network
        # Use Base Sepolia for testing, Base Mainnet for production
        wallet = Wallet.create(network_id="base-sepolia")  # Changed to base-sepolia for testing
        print(f"Wallet cretaed and details are followed {wallet}")
        if not wallet:
            return JsonResponse({
                "error": "Failed to create wallet"
            }, status=500)

        # Get the default_address in the wallet.
        address1 = wallet.default_address

        # Create another address in the wallet.
        address2 = wallet.create_address()

        # List the two addresses in the wallet.
        wallet.addresses
        
        # Export the data required to re-instantiate the wallet. The data contains the seed and the ID of the wallet.
        data = wallet.export_data()
        print(f"Data Object which is created by exporting Wallet {data}")
        # You should implement the "store" method to securely persist the data object,
        # which is required to re-instantiate the wallet at a later time. For ease of use,
        # the data object is converted to a dictionary first.
        store(data.to_dict())
        # Save the seed securely (for development purposes)
        try:
            # Pick a file to which to save your wallet seed.
            file_path = "my_seed.json"
            # Set encrypt=True to encrypt the wallet seed with your CDP secret API key.
            try:
                wallet.save_seed_to_file(file_path, encrypt=True)
                print(f"Seed for wallet {wallet.id} successfully saved to {file_path}.")
            except Exception as e:
                print(f"Error at seed is :{e}")
            
        except Exception as e:
            print(f"Error is {e}")
        try:
            faucet_transaction = wallet.faucet()

            # Wait for the faucet transaction to land on-chain.
            faucet_transaction.wait()

            print(f"Faucet transaction successfully completed: {faucet_transaction}")

            faucet_transaction.transaction_hash
            
        except Exception as E:
            print(f"Error at transaction is {e}")
            print("Transaction Failed")

    except Exception as e:
        return JsonResponse({
            "error": f"Failed to create wallet: {str(e)}"
        }, status=500)
    # Create a faucet request that returns a Faucet transaction, which can be used to retrieve the transaction hash.
    # Create response data
    response_data = {
                "message": "Wallet created successfully",
                "wallet_id": wallet.id,
                "default_address": str(address1),
                "addresses": str(wallet.addresses),
                "Wallet_status": f"Fund transferred successfully into the wallet at {faucet_transaction.transaction_link}",
                "wallet_balance" : f"Balance of the wallet is {wallet.balances()}" 
            }
    return JsonResponse(response_data)
# Helper functions

def store(data):
    """
    Implement secure storage for wallet data.
    For production, you should store this in an encrypted database.
    """
    print(f"Data object at store method {data}")
    try:
        # Get the wallet ID from the data dictionary
        wallet_id = data['wallet_id']
        if not wallet_id:
            raise Exception("Wallet ID not found in data")

        # Read existing data if file exists
        existing_data = {}
        try:
            with open('wallet_data.json', 'r') as f:
                existing_data = json.load(f)
                print(f"Existing wallet data which is in wallet_info.json file: {existing_data}")
        except FileNotFoundError:
            pass

        # Add new wallet data
        existing_data[wallet_id] = data
        print("existing_data after update")
        print(existing_data)

        # Write back to file
        with open('wallet_data.json', 'w') as f:
            json.dump(existing_data, f, indent=2)
            print(f"Successfully stored wallet data for wallet_id: {wallet_id}")
            
    except Exception as e:
        raise Exception(f"Failed to store wallet data: {str(e)}")


