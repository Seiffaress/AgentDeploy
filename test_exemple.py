from exemple_corrige import add

def test_add():
    # deux tests unitaire pour Verifier le bon fonctionnement de la fonction add 
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
