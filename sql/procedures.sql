DROP PROCEDURE IF EXISTS search_intelligence;

delimiter //
CREATE PROCEDURE search_intelligence (
    query TEXT,
    minutes_since INT
)

BEGIN

    SELECT
        id,
        MATCH (keywords) AGAINST (query) AS score,
        lastused
    FROM intelligence
    WHERE (
        MATCH (keywords) AGAINST (query) > 0
    
        AND (
            lastused IS NOT NULL
            AND timestampdiff(MINUTE , lastused, NOW()) > minutes_since
        )
    )

    ORDER BY score DESC, lastused ASC;
END//

delimiter ;
