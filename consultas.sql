/*Consulta per mostrar el nom dels treballadors i
el nom de l'empresa a la qual treballen.*/

SELECT P.Nom, E.Nom
FROM Persones AS P, Empresa AS E, Contractació AS C
WHERE P.DNI = C.DNI AND E.NIF = C.NIF;

/*Consulta per mostrar el nom dels treballadors, la ciutat, el nom de
l'empresa a la qual treballen i les dates d'Alta i Baixa*/ 

SELECT P.Nom, P.Ciutat, E.Nom, C.DataAlta, C.DataBaixa
FROM Persones AS P, Empresa AS E, Contractació AS C
WHERE P.DNI = C.DNI AND E.NIF = C.NIF;

SELECT P.Nom, P.Ciutat, E.Nom, C.DataAlta, C.DataBaixa
FROM (Persones AS P INNER JOIN Contractació AS C ON P.DNI = C.DNI)
    INNER JOIN Empreses AS E ON C.NIF=E.NIF;

SELECT 
    (SELECT Nom FROM Persones WHERE DNI=C.DNI) AS 'Nom',
    (SELECT Cognoms FROM Persones WHERE DNI=C.DNI) AS 'Cognoms',
    (SELECT Ciutat FROM Persones WHERE DNI=C.DNI) AS 'Ciutat',
    (SELECT Nom FROM Empreses WHERE NIF=C.NIF) AS 'Empresa',
    C.DataAlta,
    C.DataBaixa
FROM Contractació AS C;

/*Mostrar el DNI dels treballadors que el nom 
de la ciutat de la persona comenci per "V".*/

SELECT DNI
FROM Persones
WHERE Ciutat LIKE 'V%';

/*Modificar el contracte de tots els treballadors de 
l'empresa "Blockbuster Music" que el nom de la ciutat de la
persona comenci per "V", i posar que ha finalitzat avui.*/

UPDATE Contractació 
SET DataBaixa = date('now')
WHERE NIF = (SELECT NIF
            FROM Empresa
            WHERE Nom = 'Blockbuster Music')
    AND 
    DNI IN (SELECT DNI
           FROM Persones
           WHERE Ciutat LIKE 'V%');

/* A NIF posem el igual perque tenim nomes un valor al WHERE
mentres que a DNI poden haver-hi més d'una ciutat que començi
per V i per tant posem IN*/


/*Eliminar tots els contractes de l'empresa "Blockbuster 
Music" que ja hagin finalitzat.*/

DELETE FROM Contractació
WHERE DataBaixa IS NOT NULL
      AND
      NIF = (SELECT NIF
              FROM Empresa
              WHERE Nom = 'Blockbuster Music');

/*Comprova si hi ha algun treballador contractat en dues 
empreses al mateix temps i mostra el seu nom i cognoms.*/

/*SELECT P.Nom, P.Cognoms
FROM Persones AS P INNER JOIN Contractació AS C ON P.DNI = C.DNI
GROUP BY C.DNI
HAVING COUNT (*) > 1;

No està del tot bé, ja que si agrupem per DNI (GROUP BY) al SELECT
no podem mostrar el Nom i els Cognoms
*/

SELECT Nom, Cognoms
FROM Persones
WHERE DNI IN (SELECT DNI 
              FROM Contractació
              GROUP BY DNI
              HAVING COUNT (*)>1);

/*Modifica el cognom de les persones que tenen el cognom amb una 
'a' i una 'n' seguides, i posa'l en majúscules.*/

UPDATE Persones 
SET Cognoms= upper (Cognoms)
WHERE Cognoms LIKE '%an%';

/*Si el cognom comença per an o acaben tambe els trasformarà en majus*/

/*Mostrar els 3 primers noms que comencen per a*/

SELECT Nom
FROM Persones
WHERE Nom LIKE 'A%'
ORDER BY DESC LIMIT 3;