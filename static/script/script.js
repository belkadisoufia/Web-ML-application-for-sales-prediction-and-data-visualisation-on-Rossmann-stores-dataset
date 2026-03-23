// script.js - Version améliorée
document.addEventListener('DOMContentLoaded', function() {
    SiteLoading();
});

function AddStores()
{
    var list = document.getElementById("store-selection-list");
    if (!list) return;
    
    // Vider les options existantes (garde la première si elle existe)
    while (list.options.length > 0) {
        list.remove(0);
    }
    
    // Ajouter les magasins de 1 à 1115
    for (let i = 1; i <= 1115; i++)
    {
        var option = document.createElement("option");
        option.text = i;
        option.value = i;
        list.appendChild(option); 
    }
    console.log(`✅ ${list.options.length} magasins ajoutés`);
}

function SetDefaultDate()
{
    var date = new Date();
    var current_date = date.getFullYear().toString() + '-' + 
                      (date.getMonth() + 1).toString().padStart(2, '0') + '-' + 
                      date.getDate().toString().padStart(2, '0');
    
    var collection = document.getElementsByClassName("datepicker");
    for (let i = 0; i < collection.length; i++) {
        if (collection[i]) {
            collection[i].value = current_date;
        }
    }
    console.log(`✅ Date par défaut: ${current_date}`);
}

function ToggleSalesIndicatorsVisibility(display)
{
    if (typeof display === 'boolean')
    {
        var sales_collection = document.getElementsByClassName("sales-indicator");
        var do_display = display ? 'block' : 'none';
    
        for (let i = 0; i < sales_collection.length; i++) {
            if (sales_collection[i]) {
                sales_collection[i].style.display = do_display;
            }
        }
    }
    else
    {
        console.log("❌ L'argument n'est pas un booléen. Type: ", typeof(display));
    }
}

function ToggleResultsVisibility(display)
{
    ToggleSalesIndicatorsVisibility(display);
}

function ChangeToDateMinValue()
{
    var from_date_element = document.getElementById("from-date-selector-input");
    var to_date_element = document.getElementById("to-date-selector-input");

    if (from_date_element && to_date_element) {
        to_date_element.min = from_date_element.value;
        if (from_date_element.value > to_date_element.value)
        {
            to_date_element.value = to_date_element.min;
        }
    }
}

function ChangeFromDateMaxValue()
{
    var from_date_element = document.getElementById("from-date-selector-input");
    var to_date_element = document.getElementById("to-date-selector-input");

    if (from_date_element && to_date_element) {
        from_date_element.max = to_date_element.value;
        if (from_date_element.value > to_date_element.value)
        {
            from_date_element.value = to_date_element.value;
        }
    }
}

function ChangeButtonColor()
{
    var button = document.getElementById('predict-button');
    if (button) {
        button.style.backgroundColor = '#ffffff';
        button.style.color = '#c91f20';
    }
}

function RevertButtonColor()
{
    var button = document.getElementById('predict-button');
    if (button) {
        button.style.backgroundColor = '#c91f20';
        button.style.color = '#ffffff';
    }
}

function PredictSales()
{
    var totalElement = document.getElementById('total-sales-indicator');
    var avgElement = document.getElementById('avg-sales-indicator');
    
    if (totalElement) totalElement.innerHTML = "Calculating...";
    if (avgElement) avgElement.innerHTML = "Calculating...";

    ToggleResultsVisibility(true);
    
    // Le formulaire sera soumis normalement via POST
    return true;
}

function SiteLoading()
{
    console.log("🚀 Chargement du site...");
    AddStores();
    SetDefaultDate();
    
    // Ajouter les événements pour les boutons
    var predictButton = document.getElementById('predict-button');
    if (predictButton) {
        predictButton.addEventListener('click', function(e) {
            PredictSales();
        });
    }
    
    console.log("✅ Site chargé avec succès!");
}

// S'assurer que les fonctions sont appelées au chargement
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', SiteLoading);
} else {
    SiteLoading();
}