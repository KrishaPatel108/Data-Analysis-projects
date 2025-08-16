use competitor_analysis;
-- 1.Keywords others rank for but AgencyX does not
SELECT 
    tk.Keyword,
    ROUND(AVG(tk.SearchVolume), 0) AS AvgSearchVolume
FROM TopKeywords tk
WHERE tk.Keyword NOT IN (
    SELECT Keyword 
    FROM TopKeywords
    WHERE Competitor = 'AgencyX'
)
GROUP BY tk.Keyword
ORDER BY AvgSearchVolume DESC;



-- 2.Traffic Source Gap vs. AgencyX
SELECT 
    ts.TrafficSource,
    ROUND(AVG(CASE WHEN ts.Competitor = 'AgencyX' THEN ts.Visits END), 0) AS AgencyX_Visits,
    ROUND(AVG(CASE WHEN ts.Competitor != 'AgencyX' THEN ts.Visits END), 0) AS Competitor_Avg_Visits,
    ROUND(AVG(CASE WHEN ts.Competitor != 'AgencyX' THEN ts.Visits END) -
          AVG(CASE WHEN ts.Competitor = 'AgencyX' THEN ts.Visits END), 0) AS Gap
FROM TrafficSources ts
GROUP BY ts.TrafficSource
ORDER BY Gap DESC;

-- 3.Average posts and engagement rate per platform
SELECT 
    sm.Platform,
    ROUND(AVG(CASE WHEN sm.Competitor = 'AgencyX' THEN sm.PostsPerMonth END), 1) AS AgencyX_Posts,
    ROUND(AVG(CASE WHEN sm.Competitor != 'AgencyX' THEN sm.PostsPerMonth END), 1) AS Competitor_Avg_Posts,
    ROUND(AVG(CASE WHEN sm.Competitor = 'AgencyX' THEN sm.AvgEngagementRate END), 2) AS AgencyX_EngRate,
    ROUND(AVG(CASE WHEN sm.Competitor != 'AgencyX' THEN sm.AvgEngagementRate END), 2) AS Competitor_Avg_EngRate
FROM SocialMedia sm
GROUP BY sm.Platform;


-- Priority Keyword Score Table for AgencyX
SELECT 
    tk.Keyword,
    ROUND(AVG(tk.SearchVolume), 0) AS AvgSearchVolume,
    ROUND(21 - AVG(tk.RankingPosition), 2) AS PositionScore, -- Higher if ranked better
    ROUND( (AVG(tk.SearchVolume) * (21 - AVG(tk.RankingPosition))) / 100, 2 ) AS OpportunityScore
FROM TopKeywords tk
WHERE tk.Keyword NOT IN (
    SELECT Keyword FROM TopKeywords WHERE Competitor = 'AgencyX'
)
GROUP BY tk.Keyword
ORDER BY OpportunityScore DESC;
