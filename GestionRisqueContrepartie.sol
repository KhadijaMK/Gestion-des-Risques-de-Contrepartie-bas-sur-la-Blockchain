// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GestionRisqueContrepartie {
    // Structure définissant les attributs d'une contrepartie
    struct Contrepartie {
        address portefeuille; // Adresse unique représentant la contrepartie
        uint256 scoreCredit; // Score de crédit de la contrepartie (de 1 à 100)
        uint256 limiteExposition; // Limite maximale autorisée pour l'exposition
        uint256 expositionCourante; // Montant de l'exposition actuelle
        uint256 collaterale; // Montant du collatéral fourni par la contrepartie
        uint256 probabiliteDefaut; // Probabilité de défaut (PD) en pourcentage
        uint256 pertesEnCasDeDefaut; // Pertes potentielles en cas de défaut (LGD) en pourcentage
    }

    // Mapping associant chaque adresse de contrepartie à ses données
    mapping(address => Contrepartie) public contreparties;

    // Événements déclenchés pour signaler des changements ou dépassements
    event ContrepartieAjoutee(address indexed portefeuille, uint256 limiteExposition); // Lorsqu'une contrepartie est ajoutée
    event ExpositionMiseAJour(address indexed portefeuille, uint256 nouvelleExposition); // Lorsqu'une exposition est mise à jour
    event LimiteDepassee(address indexed portefeuille, uint256 exposition); // Si l'exposition dépasse la limite autorisée

    // Ajouter une nouvelle contrepartie avec ses données de risque
    function ajouterContrepartie(
        address _portefeuille,
        uint256 _scoreCredit,
        uint256 _limiteExposition,
        uint256 _probabiliteDefaut,
        uint256 _pertesEnCasDeDefaut,
        uint256 _collaterale
    ) public {
        // Vérifie que la contrepartie n'existe pas déjà
        require(contreparties[_portefeuille].portefeuille == address(0), "Contrepartie deja enregistree");
        // Vérifie que le score de crédit et la limite d'exposition sont valides
        require(_scoreCredit > 0 && _limiteExposition > 0, "Score de credit et limite doivent etre positifs");

        // Ajout de la contrepartie dans le mapping
        contreparties[_portefeuille] = Contrepartie({
            portefeuille: _portefeuille,
            scoreCredit: _scoreCredit,
            limiteExposition: _limiteExposition,
            expositionCourante: 0,
            collaterale: _collaterale,
            probabiliteDefaut: _probabiliteDefaut,
            pertesEnCasDeDefaut: _pertesEnCasDeDefaut
        });

        // Déclenche un événement pour signaler l'ajout
        emit ContrepartieAjoutee(_portefeuille, _limiteExposition);
    }

    // Mettre à jour l'exposition courante d'une contrepartie
    function mettreAJourExposition(address _portefeuille, uint256 _nouvelleExposition) public {
        // Vérifie que la contrepartie existe
        Contrepartie storage contrepartie = contreparties[_portefeuille];
        require(contrepartie.portefeuille != address(0), "Contrepartie non trouvee");
        // Vérifie que la nouvelle exposition n'est pas négative
        require(_nouvelleExposition >= 0, "Exposition ne peut pas etre negative");

        // Mise à jour de l'exposition courante
        contrepartie.expositionCourante = _nouvelleExposition;
        // Déclenche un événement pour notifier la mise à jour
        emit ExpositionMiseAJour(_portefeuille, _nouvelleExposition);

        // Si l'exposition dépasse la limite autorisée, émet un événement
        if (contrepartie.expositionCourante > contrepartie.limiteExposition) {
            emit LimiteDepassee(_portefeuille, contrepartie.expositionCourante);
        }
    }

    // Calculer le risque d'une contrepartie
    function calculerRisque(address _portefeuille) public view returns (uint256) {
        // Vérifie que la contrepartie existe
        Contrepartie memory contrepartie = contreparties[_portefeuille];
        require(contrepartie.portefeuille != address(0), "Contrepartie non trouvee");

        // Évite une division par zéro si la limite d'exposition est nulle
        if (contrepartie.limiteExposition == 0) {
            return 0;
        }

        // Retourne le score de risque calculé
        return (contrepartie.expositionCourante * 10000) / (contrepartie.limiteExposition * contrepartie.scoreCredit);
    }

    // Calculer le ratio de couverture
    function calculerRatioCouverture(address _portefeuille) public view returns (uint256) {
        // Vérifie que la contrepartie existe
        Contrepartie memory contrepartie = contreparties[_portefeuille];
        require(contrepartie.portefeuille != address(0), "Contrepartie non trouvee");

        // Si l'exposition courante est nulle, retourne 0 pour éviter une division par zéro
        if (contrepartie.expositionCourante == 0) {
            return 0;
        }

        // Retourne le ratio de couverture calculé
        return (contrepartie.collaterale * 100) / contrepartie.expositionCourante;
    }

    // Calculer les pertes attendues pour une contrepartie
    function calculerPertesAttendues(address _portefeuille) public view returns (uint256) {
        // Vérifie que la contrepartie existe
        Contrepartie memory contrepartie = contreparties[_portefeuille];
        require(contrepartie.portefeuille != address(0), "Contrepartie non trouvee");

        // Retourne les pertes attendues calculées
        return (contrepartie.expositionCourante * contrepartie.probabiliteDefaut * contrepartie.pertesEnCasDeDefaut) / 10000;
    }
}
