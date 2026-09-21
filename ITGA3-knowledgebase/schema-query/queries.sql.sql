SELECT variant.*, classification.classification_value
FROM variant
JOIN classification
    ON variant.variant_id = classification.variant_id
WHERE classification.classification_value IN ('Pathogenic', 'Likely pathogenic');

#unsuprsingly VUS had the highest count of 266

SELECT classification_value, COUNT(*) AS count
FROM classification
GROUP BY classification_value
ORDER BY count DESC;

#variants with no conflicst in the review status
SELECT review_status, variant_id
FROM classification
WHERE review_status ILIKE '%no conflict%';