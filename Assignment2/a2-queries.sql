
-- 1

.print \nQuestion 1 -cpatel1

SELECT DISTINCT drugs.drug_name
FROM drugs, medications, patients
WHERE patients.address LIKE '%Edmonton%'
AND medications.hcno = patients.hcno
AND medications.drug_name = drugs.drug_name
AND drugs.category = 'anti-inflammatory';


-- 2

.print \nQuestion 2 -cpatel1

SELECT s1.sym_name
FROM symptoms s1, symptoms s2, patients p1, patients p2
WHERE p1.address LIKE '%Edmonton%'
AND p2.address LIKE '%Edmonton%'
AND p1.hcno = s1.hcno
AND p2.hcno = s2.hcno
AND NOT s1.hcno = s2.hcno
AND s1.sym_name = s2.sym_name

EXCEPT 

SELECT sym_name
FROM symptoms, patients 
WHERE symptoms.hcno = patients.hcno
AND patients.address LIKE '%Calgary%';



-- 3

.print \nQuestion 3 -cpatel1

SELECT sym_name
FROM symptoms, medications
WHERE symptoms.hcno = medications.hcno
AND medications.drug_name = 'niacin'
AND symptoms.obs_date BETWEEN date(medications.mdate, '+1 day') AND date(medications.mdate, '+5 days');


-- 4 

.print \nQuestion 4 -cpatel1

SELECT group_concat(name || ':' || emg_phone, ' - ')
FROM patients, medications
WHERE patients.hcno = medications.hcno
AND medications.drug_name = 'niacin'
AND medications.days > 20
AND medications.amount > 200
GROUP BY SUBSTR( emg_phone, 0, 3);

-- 5 

.print \nQuestion 5 -cpatel1

SELECT patients.hcno, drug_name, AVG(amount), medications.amount
FROM patients, medications
WHERE medications.hcno = patients.hcno
GROUP BY drug_name, patients.age_group
HAVING MAX(medications.amount) > 2 * (SELECT AVG(AMOUNT) 
				      FROM patients p, medications m 
				      WHERE m.drug_name = medications.drug_name 
				      GROUP BY p.age_group, p.hcno);


-- 6
.print \nQuestion 6 -cpatel1

SELECT drug_name, 
sum(address LIKE '%Edmonton%')*100.0 / (SELECT count(*) FROM medications, patients WHERE address LIKE '%Edmonton%' AND medications.hcno = patients.hcno),
sum(address LIKE '%Toronto%')*100.0 /(SELECT count(*) FROM medications, patients WHERE address LIKE '%Toronto%' AND medications.hcno = patients.hcno)

FROM medications, patients

WHERE medications.hcno = patients.hcno
GROUP BY drug_name
HAVING SUM(address LIKE '%Edmonton%')*1.0/(SELECT count(*) FROM medications, patients WHERE address LIKE '%Edmonton%' AND medications.hcno = patients.hcno) 
> SUM(address LIKE '%Toronto%')*1.0/(SELECT count(*) FROM medications, patients WHERE address LIKE '%Toronto%' AND medications.hcno = patients.hcno) ;

-- 7
.print \nQuestion 7 -cpatel1

SELECT drug_name, AVG(amount), SUM(amount * days)
FROM medications 
GROUP BY drug_name
HAVING AVG(DAYS) > 3
AND drug_name IN (SELECT drug_name 
		  FROM medications, patients, symptoms
		  WHERE patients.hcno = symptoms.hcno
		  AND medications.hcno = patients.hcno 
		  AND sym_name = 'headache'
		  AND date(mdate) = date(obs_date)); 

-- 8 

.print \nQuestion 8 -cpatel1

SELECT r1.hcno
FROM reportedallergies r1
WHERE r1.hcno != 23769
AND r1.drug_name IN (SELECT drug_name FROM reportedallergies WHERE hcno = 23769)

EXCEPT 

SELECT hcno
FROM reportedallergies ra
WHERE hcno != 23769
AND drug_name NOT IN (SELECT drug_name FROM reportedallergies WHERE hcno = 23769)

EXCEPT 

SELECT hcno
FROM reportedallergies ra
WHERE hcno != 23769
GROUP BY hcno
HAVING count(*) != (SELECT COUNT(*) FROM reportedallergies WHERE hcno = 23769);



-- 9 

.print \nQuestion 9 -cpatel1


DROP VIEW IF EXISTS allergies;
CREATE VIEW allergies

AS SELECT hcno, drug_name AS drug_name
FROM (SELECT hcno, drug_name
      FROM reportedallergies ra LEFT OUTER JOIN inferredallergies ia ON drug_name = alg
      UNION 
      SELECT hcno, canbe_alg
      FROM reportedallergies ra LEFT OUTER JOIN inferredallergies ia ON drug_name = alg)
      WHERE drug_name NOT NULL;

SELECT * FROM allergies;

-- 10

.print \nQuestion 10 -cpatel1

SELECT DISTINCT drugs.drug_name 
FROM drugs, allergies 
WHERE allergies.hcno = 23769
AND drugs.drug_name NOT IN (SELECT allergies.drug_name FROM allergies WHERE allergies.hcno = 23769)
AND drugs.category = 'anti-inflammatory'; 

