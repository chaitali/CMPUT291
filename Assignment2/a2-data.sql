

INSERT INTO patients VALUES

('23769', 'Patient O', '0-10', '123 St, 10 Ave Edmonton', '780-123-4567', '780-123-4567'),
('10000', 'Patient 1', '0-10', '345 St, 10 Ave Edmonton', '780-333-4567', '587-123-4567'),
('20000', 'Patient 2', '10-15', '567 St, 10 Ave Edmonton', '587-143-4567', '780-444-4567'),
('30000', 'Patient 3', '10-15', '444 St, 10 Ave Edmonton', '587-555-4567', '780-555-4567'),
('40000', 'Patient 4', '0-10', '10 St 50 Ave Calgary', '666-111-6666', '666-555-5555'),
('50000', 'Patient 5', '0-10', '10 St 60 Ave Calgary', '666-333-6666', '666-565-5555'),
('60000', 'Patient 6', '10-15', '10 St 70 Ave Calgary', '666-444-6666', '666-575-5555'),
('70000', 'Patient 7', '0-10', '424 21St Toronto', '789-989-0000', '910-898-0000'),
('80000', 'Patient 8', '10-15', '434 22St Toronto', '500-969-0000', '920-898-0000');


INSERT INTO symptoms VALUES

('10000', '2013-10-07 08:23:19.120', 'headache'),  --same date two symptoms, edmonton
('10000', '2013-10-07 08:23:19.120', 'migraine'),  -- edmonton
('20000', '2013-10-03 08:23:19.120', 'headache'),  --diff date headache, edmonton
('30000', '2013-10-04 08:23:19.120', 'headache'),  --same date headache,  edmonton
('30000', '2013-10-11 08:23:19.120', 'sore muscles'), --edmonton
('23769', '2013-10-15 08:23:19.120', 'sore muscles'), --edmonton
('70000', '2013-10-15 08:23:19.120', 'migraine'), --toronto
('40000', '2013-10-07 08:23:19.120', 'sore muscles'); --calgary

INSERT INTO drugs VALUES
('niacin', 'anti-inflammatory'),
('ibuprofen', 'anti-inflammatory'),
('drug2', 'antibiotic');

INSERT INTO medications VALUES
('40000', '2013-10-03 08:23:19.120', 400, 1, 'niacin'), --calgary
('10000', '2013-10-07 08:23:19.120', 1, 1, 'niacin'),  --edmonton
('23769', '2013-10-09 08:23:19.120', 10, 300, 'drug2'), --edmonton
('20000', '2013-10-07 08:23:19.120', 50, 7, 'ibuprofen'), --edmonton
('10000', '2013-10-08 08:23:19.120', 5, 1, 'niacin'), --edmonton
('70000', '2013-10-03 08:23:19.120', 1, 30, 'drug2'), --toronto
('30000', '2013-10-05 08:23:19.120', 10, 1, 'niacin'), --edmonton
('30000', '2013-10-04 08:23:19.120', 1000, 1, 'niacin'); --edmonton



INSERT INTO reportedallergies VALUES
('10000', 'drug2'),
('10000', 'niacin'),
('23769', 'drug2'),
('30000', 'ibuprofen'),
('23769', 'niacin'),
('30000', 'drug2'),
('30000', 'niacin');


INSERT INTO inferredallergies VALUES
('ibuprofen', 'niacin');
