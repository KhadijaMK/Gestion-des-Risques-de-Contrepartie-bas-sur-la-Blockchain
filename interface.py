import streamlit as st
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Infura project URL (replace with your own project ID)
infura_url = "https://polygon-amoy.infura.io/v3/97665b40b4fd4219aca063f99de5d01a"
web3 = Web3(Web3.HTTPProvider(infura_url))

st.set_page_config(
    page_title="Gestion des Risques Contreparties",
    page_icon="Logo.png",
    layout="wide"
)

# Sidebar navigation
st.sidebar.image("Welcome_Poster-removebg-preview.png")
menu = st.sidebar.radio("", [
    "Accueil",
    "Ajouter une Contrepartie",
    "Mettre à Jour Exposition",
    "Calcul des Risques et Ratios",
    "Tout les informations"
])

# Check connection
st.image("Profile-Banner.png")
if web3.is_connected():
    st.sidebar.success("✅ Connecté au réseau Infura")
else:
    st.sidebar.error("❌ Échec de connexion à Infura")
    st.stop()

# Load private key from the .env file
private_key = os.getenv("PRIVATE_KEY")
if not private_key:
    st.sidebar.error("🔒 Clé privée non trouvée! Veuillez l'ajouter dans le fichier .env.")
    st.stop()

# Get the wallet address from the private key
account = Account.from_key(private_key)
portefeuille = account.address
st.sidebar.info(f"🔑 Adresse du Portefeuille: {portefeuille}")

# Smart Contract details
contract_address = Web3.to_checksum_address("0x69edc9986339f031a1fb7a77eb97ee9feb9e407e")
contract_abi = [ 
    {
        "inputs": [
            {"internalType": "address", "name": "_portefeuille", "type": "address"},
            {"internalType": "uint256", "name": "_scoreCredit", "type": "uint256"},
            {"internalType": "uint256", "name": "_limiteExposition", "type": "uint256"},
            {"internalType": "uint256", "name": "_probabiliteDefaut", "type": "uint256"},
            {"internalType": "uint256", "name": "_pertesEnCasDeDefaut", "type": "uint256"},
            {"internalType": "uint256", "name": "_collaterale", "type": "uint256"}
        ],
        "name": "ajouterContrepartie",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_portefeuille", "type": "address"},
            {"internalType": "uint256", "name": "_nouvelleExposition", "type": "uint256"}
        ],
        "name": "mettreAJourExposition",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "_portefeuille", "type": "address"}],
        "name": "calculerRisque",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "_portefeuille", "type": "address"}],
        "name": "calculerRatioCouverture",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "_portefeuille", "type": "address"}],
        "name": "calculerPertesAttendues",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "contreparties",
		"outputs": [
			{
				"internalType": "address",
				"name": "portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "scoreCredit",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "limiteExposition",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "expositionCourante",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "collaterale",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "probabiliteDefaut",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "pertesEnCasDeDefaut",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
   

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Main content based on the selected menu
if menu == "Accueil":
    st.header("Bienvenue sur l'outil de Gestion des Risques de Contrepartie ")
    st.write('Cet outil basé sur la technologie blockchain permet de simplifier et de sécuriser la gestion des contreparties financières en exploitant la puissance du réseau . Vous y trouverez plusieurs fonctionnalités essentielles pour surveiller et optimiser vos expositions. ')
    st.header('Ajouter une Contrepartie :') 
    st.write('Enregistrez de nouvelles contreparties en renseignant des données clés telles que le score de crédit, la limite d\'exposition...')
    st.header('Mise à Jour des Expositions : ') 
    st.write('Modifiez les niveaux d\'exposition associés à vos contreparties de manière fluide et sécurisée.')
    st.header('Calcul des Risques et Ratios : ') 
    st.write('Analysez les risques financiers associés à vos contreparties à travers des indicateurs tels que le score de risque, le ratio de couverture, et les pertes attendues.')
    st.info("Vous pouvez maintenant gérer vos contreparties.")

elif menu == "Ajouter une Contrepartie":
    st.header("Ajouter une Contrepartie")
    score_credit = st.number_input("Score de Crédit", min_value=1, value=100)
    limite_exposition = st.number_input("Limite d'Exposition", min_value=1, value=1000)
    probabilite_defaut = st.number_input("Probabilité de Défaut (%)", min_value=0, max_value=100, value=10)
    pertes_defaut = st.number_input("Pertes en Cas de Défaut (%)", min_value=0, max_value=100, value=50)
    collaterale = st.number_input("Montant du Collatéral", min_value=0, value=500)

    if st.button("Ajouter Contrepartie"):
        try:
            nonce = web3.eth.get_transaction_count(portefeuille)
            txn = contract.functions.ajouterContrepartie(
                portefeuille,
                int(score_credit),
                int(limite_exposition),
                int(probabilite_defaut),
                int(pertes_defaut),
                int(collaterale)
            ).build_transaction({
                "from": portefeuille,
                "nonce": nonce,
                "gas": 300000,
                "gasPrice": web3.to_wei("30", "gwei")
            })
            signed_txn = web3.eth.account.sign_transaction(txn, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
            st.success(f"Contrepartie ajoutée avec succès! Transaction hash: {tx_hash.hex()}")
        except Exception as e:
            st.error(f"Erreur lors de l'ajout de la contrepartie: {e}")

elif menu == "Mettre à Jour Exposition":
    st.header("Mettre à Jour l'Exposition")
    nouvelle_exposition = st.number_input("Nouvelle Exposition", min_value=0, value=0)

    if st.button("Mettre à Jour Exposition"):
        if nouvelle_exposition > limite_exposition:
            st.error(f"❌ Exposition dépasse la limite autorisée de {limite_exposition}!")
            try:
                nonce = web3.eth.get_transaction_count(portefeuille)
                txn = contract.functions.mettreAJourExposition(
                    portefeuille,
                    int(nouvelle_exposition)
                ).build_transaction({
                    "from": portefeuille,
                    "nonce": nonce,
                    "gas": 200000,
                    "gasPrice": web3.to_wei("30", "gwei")
                })
                signed_txn = web3.eth.account.sign_transaction(txn, private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                st.success(f"Transaction envoyée mais refusée. Vous pouvez vérifier la transaction sur PolygonScan : [Voir Transaction](https://amoy.polygonscan.com/address/{contract_address})")
            except Exception as e:
                st.error(f"Erreur lors de la mise à jour de l'exposition: {e}")
        else:
            try:
                nonce = web3.eth.get_transaction_count(portefeuille)
                txn = contract.functions.mettreAJourExposition(
                    portefeuille,
                    int(nouvelle_exposition)
                ).build_transaction({
                    "from": portefeuille,
                    "nonce": nonce,
                    "gas": 200000,
                    "gasPrice": web3.to_wei("30", "gwei")
                })
                signed_txn = web3.eth.account.sign_transaction(txn, private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                st.success(f"Exposition mise à jour avec succès! Transaction hash: {tx_hash.hex()}")
            except Exception as e:
                st.error(f"Erreur lors de la mise à jour de l'exposition: {e}")

elif menu == "Calcul des Risques et Ratios":
    st.header("Calcul des Risques et Ratios")
    if st.button("Cliquez pour calculer "):
        try:
            risque = contract.functions.calculerRisque(portefeuille).call()
            ratio_couverture = contract.functions.calculerRatioCouverture(portefeuille).call()
            pertes_attendues = contract.functions.calculerPertesAttendues(portefeuille).call()

            st.write(f"Score de Risque : {risque}")
            st.write(f"Ratio de Couverture : {ratio_couverture}%")
            st.write(f"Pertes Attendues : {pertes_attendues}")
        except Exception as e:
            st.error(f"Erreur lors du calcul des risques et ratios: {e}")
elif menu == "Tout les informations":
    if st.button("Afficher Informations"):
        try: 
            contrepartie_info = contract.functions.contreparties(portefeuille).call()
            if contrepartie_info[0] != "0x0000000000000000000000000000000000000000":
                st.json({
                    "Portefeuille": contrepartie_info[0],
                    "Score de Crédit": contrepartie_info[1],
                    "Limite d'Exposition": contrepartie_info[2],
                    "Exposition Courante": contrepartie_info[3],
                    "Collateral": contrepartie_info[4],
                    "Probabilité de Défaut": contrepartie_info[5],
                    "Pertes en Cas de Défaut": contrepartie_info[6]
                })
            else:
                st.warning("Aucune contrepartie trouvée.")
        except Exception as e:
            st.error(f"Erreur : {e}")
# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 *Note:* Utilisez toujours des réseaux de test pour les expérimentations.")
