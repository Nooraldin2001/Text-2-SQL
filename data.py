data = [
    {
      "Prompt": "As part of the company's efforts to improve employee retention, develop a SQL query that provides an in-depth analysis of employee engagement and satisfaction. The query should offer the following insights:\n\n1. Engagement and Satisfaction Trends: Calculate the average engagement and satisfaction scores for employees grouped by department.\n2. High Performers: Identify employees with an engagement score above 90 and a satisfaction score above 85. Provide their names, job titles, and departments.\n3. Gender Representation: Determine the proportion of male, female, and non-binary employees in each department. Include department name, gender, and percentages.",
      "Response": "WITH AvgScores AS (\n    SELECT department_type, \n           AVG(engagement_score) AS avg_engagement, \n           AVG(satisfaction_score) AS avg_satisfaction\n    FROM employee_engagement_survey_data e\n    JOIN employee_data d ON e.employee_id = d.employee_id\n    GROUP BY department_type\n),\nHighPerformers AS (\n    SELECT d.first_name, d.last_name, d.title, d.department_type\n    FROM employee_engagement_survey_data e\n    JOIN employee_data d ON e.employee_id = d.employee_id\n    WHERE e.engagement_score > 90 AND e.satisfaction_score > 85\n),\nGenderRepresentation AS (\n    SELECT d.department_type, d.gender, \n           COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY d.department_type) AS percentage\n    FROM employee_data d\n    GROUP BY d.department_type, d.gender\n)\nSELECT * FROM AvgScores\nUNION ALL\nSELECT * FROM HighPerformers\nUNION ALL\nSELECT * FROM GenderRepresentation;"
    },
    {
      "Prompt": "To optimize the company's training programs, create a SQL query that identifies key patterns in training data. The query should provide the following insights:\n\n1. Training Completion Rates: Calculate the percentage of employees who have completed their training programs in each business unit.\n2. High-Cost Training: Identify training programs that cost more than $5000. Provide their names, duration, and associated trainer.\n3. Correlation with Performance: Find employees who completed training in 'Leadership' and have a performance score of 'Excellent'. Provide their names, job titles, and business units.",
      "Response": "WITH CompletionRates AS (\n    SELECT d.business_unit, \n           COUNT(CASE WHEN t.training_outcome = 'Completed' THEN 1 END) * 100.0 / COUNT(*) AS completion_rate\n    FROM training_and_development_data t\n    JOIN employee_data d ON t.employee_id = d.employee_id\n    GROUP BY d.business_unit\n),\nHighCostTraining AS (\n    SELECT training_program_name, training_duration_days, trainer\n    FROM training_and_development_data\n    WHERE training_cost > 5000\n),\nPerformanceCorrelation AS (\n    SELECT d.first_name, d.last_name, d.title, d.business_unit\n    FROM training_and_development_data t\n    JOIN employee_data d ON t.employee_id = d.employee_id\n    WHERE t.training_program_name = 'Leadership' AND d.performance_score = 'Excellent'\n)\nSELECT * FROM CompletionRates\nUNION ALL\nSELECT * FROM HighCostTraining\nUNION ALL\nSELECT * FROM PerformanceCorrelation;"
    },
    {
      "Prompt": "To support recruitment strategy improvements, create a SQL query that provides insights into applicant data. The query should include the following:\n\n1. Education Distribution: Group applicants by their highest education level and count the number in each group.\n2. Experience Analysis: Calculate the average years of experience for applicants grouped by job title.\n3. Geographic Distribution: Count the number of applicants from each state.",
      "Response": "WITH EducationDistribution AS (\n    SELECT education_level, COUNT(*) AS count\n    FROM recruitment_data\n    GROUP BY education_level\n),\nExperienceAnalysis AS (\n    SELECT job_title, AVG(years_of_experience) AS avg_experience\n    FROM recruitment_data\n    GROUP BY job_title\n),\nGeographicDistribution AS (\n    SELECT state, COUNT(*) AS applicant_count\n    FROM recruitment_data\n    GROUP BY state\n)\nSELECT * FROM EducationDistribution\nUNION ALL\nSELECT * FROM ExperienceAnalysis\nUNION ALL\nSELECT * FROM GeographicDistribution;"
    },
    {
      "Prompt": """As part of the company's workforce analysis, create a SQL query to explore the distribution and performance of employees. The query should include the following insights:
                    1. Performance Distribution: Calculate the average performance score for each employee type (Full-time, Part-time, Contract).
                    2. Termination Analysis: Identify the number of employees terminated by each termination type.
                    3. Regional Performance: Determine the average performance score of employees grouped by state.""",
      "Response": """WITH PerformanceDistribution AS (
                     SELECT employee_type, AVG(performance_score) AS avg_performance
                     FROM employee_data
                     GROUP BY employee_type
                     ),
                     TerminationAnalysis AS (
                         SELECT termination_type, COUNT(*) AS termination_count
                         FROM employee_data
                         GROUP BY termination_type
                     ),
                     RegionalPerformance AS (
                         SELECT state, AVG(performance_score) AS avg_performance
                         FROM employee_data
                         GROUP BY state
                     )
                     SELECT * FROM PerformanceDistribution
                     UNION ALL
                     SELECT * FROM TerminationAnalysis
                     UNION ALL
                     SELECT * FROM RegionalPerformance;"""
    },
    {
      "Prompt": """To assist in evaluating training investments, generate a SQL query that examines the effectiveness and cost distribution of training programs. Include the following:
                1. Training Effectiveness: Calculate the percentage of employees who completed their training programs by training type.
                2. Costly Programs: Identify training programs that exceeded a cost threshold of $7000. Include program name, cost, and trainer.
                3. Departmental Training: Determine the total training cost for each department.""",
        "Response": """WITH TrainingEffectiveness AS (
                    SELECT training_type, COUNT(CASE WHEN training_outcome = 'Completed' THEN 1 END) * 100.0 / COUNT(*) AS completion_rate
                    FROM training_and_development_data
                    GROUP BY training_type
                ),
                CostlyPrograms AS (
                    SELECT training_program_name, training_cost, trainer
                    FROM training_and_development_data
                    WHERE training_cost > 7000
                ),
                DepartmentalTraining AS (
                    SELECT d.department_type, SUM(t.training_cost) AS total_cost
                    FROM training_and_development_data t
                    JOIN employee_data d ON t.employee_id = d.employee_id
                    GROUP BY d.department_type
                )
                SELECT * FROM TrainingEffectiveness
                UNION ALL
                SELECT * FROM CostlyPrograms
                UNION ALL
                SELECT * FROM DepartmentalTraining;"""
    },
    {
      "Prompt": """To improve work-life balance strategies, generate a SQL query that analyzes survey data. Include the following:
                1. Work-Life Balance Trends: Calculate the average work-life balance score for employees in each business unit.
                2. High Satisfaction Employees: Identify employees with a satisfaction score above 90. Provide their names, job titles, and business units.
                3. Correlation Analysis: Compare the average engagement score of employees with a work-life balance score below 50 versus those above 80.""",
      "Response": """WITH WorkLifeBalanceTrends AS (
                   SELECT business_unit, AVG(work_life_balance_score) AS avg_balance
                   FROM employee_engagement_survey_data e
                   JOIN employee_data d ON e.employee_id = d.employee_id
                   GROUP BY business_unit
                   ),
                   HighSatisfactionEmployees AS (
                       SELECT d.first_name, d.last_name, d.title, d.business_unit
                       FROM employee_engagement_survey_data e
                       JOIN employee_data d ON e.employee_id = d.employee_id
                       WHERE e.satisfaction_score > 90
                   ),
                   CorrelationAnalysis AS (
                       SELECT CASE WHEN work_life_balance_score < 50 THEN 'Low' ELSE 'High' END AS balance_group,
                              AVG(engagement_score) AS avg_engagement
                       FROM employee_engagement_survey_data
                       GROUP BY balance_group
                   )
                   SELECT * FROM WorkLifeBalanceTrends
                   UNION ALL
                   SELECT * FROM HighSatisfactionEmployees
                   UNION ALL
                   SELECT * FROM CorrelationAnalysis;"""
    },
    {
      "Prompt": """To streamline recruitment efforts, create a SQL query that evaluates applicant trends and preferences. Include the following:
                1. Application Trends: Count the number of applications received each month in the last year.
                2. Preferred Roles: Identify the top 5 job titles with the highest number of applicants. Include the count of applicants for each.
                3. Education Insights: Calculate the average years of experience for applicants grouped by their highest education level.""",
      "Response": """WITH ApplicationTrends AS (
    SELECT strftime('%Y-%m', application_date) AS application_month, COUNT(*) AS count
    FROM recruitment_data
    WHERE application_date >= date('now', '-1 year')
    GROUP BY application_month
    ),
    PreferredRoles AS (
        SELECT job_title, COUNT(*) AS applicant_count
        FROM recruitment_data
        GROUP BY job_title
        ORDER BY applicant_count DESC
        LIMIT 5
    ),
    EducationInsights AS (
        SELECT education_level, AVG(years_of_experience) AS avg_experience
        FROM recruitment_data
        GROUP BY education_level
    )
    SELECT * FROM ApplicationTrends
    UNION ALL
    SELECT * FROM PreferredRoles
    UNION ALL
    SELECT * FROM EducationInsights;"""
    },
    {
      "Prompt": """To evaluate employee engagement in different business units, create a SQL query that provides the following insights:
            1. Engagement by Unit: Calculate the average engagement score for each business unit.
            2. Top Performers: Identify employees with engagement scores in the top 10% across all business units. Include their names and job titles.
            3. Unit Satisfaction: Determine the average satisfaction score for employees in each business unit.""",
      "Response": """WITH EngagementByUnit AS (
    SELECT business_unit, AVG(engagement_score) AS avg_engagement
    FROM employee_engagement_survey_data e
    JOIN employee_data d ON e.employee_id = d.employee_id
    GROUP BY business_unit
    ),
    TopPerformers AS (
        SELECT d.first_name, d.last_name, d.title
        FROM employee_engagement_survey_data e
        JOIN employee_data d ON e.employee_id = d.employee_id
        WHERE e.engagement_score > (SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY engagement_score) FROM employee_engagement_survey_data)
    ),
    UnitSatisfaction AS (
        SELECT business_unit, AVG(satisfaction_score) AS avg_satisfaction
        FROM employee_engagement_survey_data e
        JOIN employee_data d ON e.employee_id = d.employee_id
        GROUP BY business_unit
    )
    SELECT * FROM EngagementByUnit
    UNION ALL
    SELECT * FROM TopPerformers
    UNION ALL
    SELECT * FROM UnitSatisfaction;"""
    },
    {
      "Prompt": """To enhance training program evaluation, create a SQL query that provides insights into training outcomes. Include the following:
            1. Completion Rates by Program: Calculate the completion rate for each training program.
            2. High-Cost Trainings: Identify training programs that exceed $10,000 in total cost. Include their names and the number of attendees.
            3. Impactful Trainings: Find employees who completed the 'Advanced Technical Skills' training and achieved an engagement score above 85. Include their names and job titles.""",
      "Response": """WITH CompletionRatesByProgram AS (
            SELECT training_program_name, COUNT(CASE WHEN training_outcome = 'Completed' THEN 1 END) * 100.0 / COUNT(*) AS completion_rate
            FROM training_and_development_data
            GROUP BY training_program_name
            ),
            HighCostTrainings AS (
                SELECT training_program_name, SUM(training_cost) AS total_cost, COUNT(employee_id) AS attendees
                FROM training_and_development_data
                WHERE training_cost > 10000
                GROUP BY training_program_name
            ),
            ImpactfulTrainings AS (
                SELECT d.first_name, d.last_name, d.title
                FROM training_and_development_data t
                JOIN employee_data d ON t.employee_id = d.employee_id
                JOIN employee_engagement_survey_data e ON d.employee_id = e.employee_id
                WHERE t.training_program_name = 'Advanced Technical Skills' AND e.engagement_score > 85
            )
            SELECT * FROM CompletionRatesByProgram
            UNION ALL
            SELECT * FROM HighCostTrainings
            UNION ALL
            SELECT * FROM ImpactfulTrainings;"""
    },
    {
      "Prompt": """To analyze employee performance and retention, create a SQL query to identify key patterns. Include the following insights:
            1. Retention Rates: Calculate the percentage of employees retained over the last three years.
            2. Top Performers by Department: Identify the top 3 employees with the highest performance scores in each department. Include their names and scores.
            3. Exit Trends: Count the number of employees who exited the company each year.""",
      "Response": """WITH RetentionRates AS (
            SELECT strftime('%Y', start_date) AS start_year, 
                   COUNT(CASE WHEN exit_date IS NULL THEN 1 END) * 100.0 / COUNT(*) AS retention_rate
            FROM employee_data
            WHERE strftime('%Y', start_date) >= strftime('%Y', 'now', '-3 years')
            GROUP BY start_year
            ),
            TopPerformers AS (
                SELECT department_type, first_name, last_name, performance_score
                FROM (
                    SELECT d.department_type, d.first_name, d.last_name, d.performance_score,
                           RANK() OVER (PARTITION BY d.department_type ORDER BY d.performance_score DESC) AS rank
                    FROM employee_data d
                )
                WHERE rank <= 3
            ),
            ExitTrends AS (
                SELECT strftime('%Y', exit_date) AS exit_year, COUNT(*) AS exit_count
                FROM employee_data
                WHERE exit_date IS NOT NULL
                GROUP BY exit_year
            )
            SELECT * FROM RetentionRates
            UNION ALL
            SELECT * FROM TopPerformers
            UNION ALL
            SELECT * FROM ExitTrends;"""
    },
    {
      "Prompt": """To evaluate diversity initiatives, create a SQL query that analyzes employee demographics. Include the following:
        1. Gender Distribution: Calculate the percentage of employees by gender in each department.
        2. Ethnicity Representation: Count the number of employees from each ethnicity in each business unit.
        3. Salary Averages: Determine the average pay zone for employees grouped by gender and ethnicity.""",
      "Response": """WITH GenderDistribution AS (
            SELECT department_type, gender, 
                   COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY department_type) AS percentage
            FROM employee_data
            GROUP BY department_type, gender
            ),
            EthnicityRepresentation AS (
                SELECT business_unit, race_ethnicity, COUNT(*) AS count
                FROM employee_data
                GROUP BY business_unit, race_ethnicity
            ),
            SalaryAverages AS (
                SELECT gender, race_ethnicity, AVG(pay_zone) AS avg_pay_zone
                FROM employee_data
                GROUP BY gender, race_ethnicity
            )
            SELECT * FROM GenderDistribution
            UNION ALL
            SELECT * FROM EthnicityRepresentation
            UNION ALL
            SELECT * FROM SalaryAverages;"""
    },
    {
      "Prompt": """To monitor employee growth, create a SQL query that tracks changes in performance scores over time. Include the following:
            1. Yearly Performance Growth: Calculate the average performance score for each year across all employees.
            2. Top 5 Improving Employees: Identify the top 5 employees with the largest improvement in performance score from the previous year. Include their names and scores.
            3. Department Growth Trends: Determine the yearly average performance score for each department.""",
      "Response": """WITH YearlyPerformanceGrowth AS (
            SELECT strftime('%Y', start_date) AS year, AVG(performance_score) AS avg_performance
            FROM employee_data
            GROUP BY year
            ),
            TopImprovingEmployees AS (
                SELECT d.first_name, d.last_name, 
                       (e.performance_score - LAG(e.performance_score) OVER (PARTITION BY e.employee_id ORDER BY e.survey_date)) AS improvement
                FROM employee_engagement_survey_data e
                JOIN employee_data d ON e.employee_id = d.employee_id
                ORDER BY improvement DESC
                LIMIT 5
            ),
            DepartmentGrowthTrends AS (
                SELECT d.department_type, strftime('%Y', start_date) AS year, AVG(e.performance_score) AS avg_score
                FROM employee_engagement_survey_data e
                JOIN employee_data d ON e.employee_id = d.employee_id
                GROUP BY d.department_type, year
            )
            SELECT * FROM YearlyPerformanceGrowth
            UNION ALL
            SELECT * FROM TopImprovingEmployees
            UNION ALL
            SELECT * FROM DepartmentGrowthTrends;"""
    },
    {
      "Prompt": """To evaluate employee attendance in training programs, create a SQL query that provides insights into training participation. Include the following:
            1. Training Attendance: Count the number of employees who attended each training program.
            2. Department Participation: Calculate the percentage of employees in each department who have attended at least one training program.
            3. High Attendance Programs: Identify training programs with more than 50 attendees. Include the program name and number of attendees.""",
      "Response": """WITH TrainingAttendance AS (
            SELECT training_program_name, COUNT(employee_id) AS attendee_count
            FROM training_and_development_data
            GROUP BY training_program_name
            ),
            DepartmentParticipation AS (
                SELECT d.department_type, 
                       COUNT(DISTINCT t.employee_id) * 100.0 / COUNT(DISTINCT d.employee_id) AS participation_rate
                FROM employee_data d
                LEFT JOIN training_and_development_data t ON d.employee_id = t.employee_id
                GROUP BY d.department_type
            ),
            HighAttendancePrograms AS (
                SELECT training_program_name, COUNT(employee_id) AS attendee_count
                FROM training_and_development_data
                GROUP BY training_program_name
                HAVING attendee_count > 50
            )
            SELECT * FROM TrainingAttendance
            UNION ALL
            SELECT * FROM DepartmentParticipation
            UNION ALL
            SELECT * FROM HighAttendancePrograms;"""
    },
    {
      "Prompt": "To identify active employees, write a SQL query that lists all employees currently employed. Include their names and job titles.",
      "Response": "SELECT first_name, last_name, title\nFROM employee_data\nWHERE employee_status = 'Active';"
    },
    {
      "Prompt": "To evaluate training participation, write a SQL query that counts the number of employees who completed training programs.",
      "Response": "SELECT COUNT(*) AS completed_trainings\nFROM training_and_development_data\nWHERE training_outcome = 'Completed';"
    },
    {
      "Prompt": "To understand recruitment trends, write a SQL query that calculates the number of applications received for each job title.",
      "Response": "SELECT job_title, COUNT(*) AS application_count\nFROM recruitment_data\nGROUP BY job_title;"
    },
    {
      "Prompt": "To analyze diversity, write a SQL query that calculates the percentage of employees by gender.",
      "Response": "SELECT gender, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage\nFROM employee_data\nGROUP BY gender;"
    },
    {
      "Prompt": "To evaluate engagement scores, write a SQL query that finds the average engagement score for each department.",
      "Response": "SELECT department_type, AVG(engagement_score) AS avg_engagement\nFROM employee_engagement_survey_data e\nJOIN employee_data d ON e.employee_id = d.employee_id\nGROUP BY department_type;"
    },
    {
      "Prompt": "To track employee growth, write a SQL query that lists employees who have been with the company for over 5 years. Include their names and start dates.",
      "Response": "SELECT first_name, last_name, start_date\nFROM employee_data\nWHERE julianday('now') - julianday(start_date) > 5 * 365;"
    },
    {
      "Prompt": "To improve satisfaction strategies, write a SQL query that lists employees with a satisfaction score above 80. Include their names and departments.",
      "Response": "SELECT d.first_name, d.last_name, d.department_type\nFROM employee_engagement_survey_data e\nJOIN employee_data d ON e.employee_id = d.employee_id\nWHERE e.satisfaction_score > 80;"
    },
    {
      "Prompt": "To evaluate training costs, write a SQL query that calculates the total cost of training programs for each department.",
      "Response": "SELECT d.department_type, SUM(t.training_cost) AS total_training_cost\nFROM training_and_development_data t\nJOIN employee_data d ON t.employee_id = d.employee_id\nGROUP BY d.department_type;"
    },
    {
      "Prompt": "To analyze recruitment success, write a SQL query that counts the number of applicants selected for each job title.",
      "Response": "SELECT job_title, COUNT(*) AS selected_count\nFROM recruitment_data\nWHERE status = 'Selected'\nGROUP BY job_title;"
    },
    {
      "Prompt": "To track work-life balance, write a SQL query that finds the average work-life balance score for employees in each business unit.",
      "Response": "SELECT business_unit, AVG(work_life_balance_score) AS avg_balance\nFROM employee_engagement_survey_data e\nJOIN employee_data d ON e.employee_id = d.employee_id\nGROUP BY business_unit;"
    },
    {
      "Prompt": "To monitor exit trends, write a SQL query that counts the number of employees who exited the company each year.",
      "Response": "SELECT strftime('%Y', exit_date) AS exit_year, COUNT(*) AS exit_count\nFROM employee_data\nWHERE exit_date IS NOT NULL\nGROUP BY exit_year;"
    },
    {
      "Prompt": "To analyze performance, write a SQL query that identifies the top 3 employees with the highest performance scores in each department.",
      "Response": "SELECT department_type, first_name, last_name, performance_score\nFROM (\n    SELECT department_type, first_name, last_name, performance_score,\n           RANK() OVER (PARTITION BY department_type ORDER BY performance_score DESC) AS rank\n    FROM employee_data\n)\nWHERE rank <= 3;"
    },
    {
      "Prompt": "To analyze department retention, write a SQL query that calculates the retention rate for each department.",
      "Response": "SELECT department_type, \n           COUNT(CASE WHEN employee_status = 'Active' THEN 1 END) * 100.0 / COUNT(*) AS retention_rate\nFROM employee_data\nGROUP BY department_type;"
    },
    {
      "Prompt": "To understand salary distribution, write a SQL query that calculates the average pay zone for each job title.",
      "Response": "SELECT title, AVG(pay_zone) AS avg_pay_zone\nFROM employee_data\nGROUP BY title;"
    },
    {
      "Prompt": "To find inactive employees, write a SQL query that lists employees who are no longer employed. Include their names and termination types.",
      "Response": "SELECT first_name, last_name, termination_type\nFROM employee_data\nWHERE employee_status = 'Terminated';"
    },
    {
      "Prompt": "To assess training impact, write a SQL query that lists employees who completed 'Leadership' training and their current performance scores.",
      "Response": "SELECT d.first_name, d.last_name, d.performance_score\nFROM training_and_development_data t\nJOIN employee_data d ON t.employee_id = d.employee_id\nWHERE t.training_program_name = 'Leadership' AND t.training_outcome = 'Completed';"
    },
    {
      "Prompt": "To analyze job function diversity, write a SQL query that counts the number of employees in each job function.",
      "Response": "SELECT job_function, COUNT(*) AS employee_count\nFROM employee_data\nGROUP BY job_function;"
    },
    {
      "Prompt": "To evaluate applicant experience, write a SQL query that calculates the average years of experience for applicants grouped by state.",
      "Response": "SELECT state, AVG(years_of_experience) AS avg_experience\nFROM recruitment_data\nGROUP BY state;"
    },
    {
      "Prompt": "To understand gender representation in management, write a SQL query that calculates the percentage of male and female employees in management roles.",
      "Response": "SELECT gender, \n           COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage\nFROM employee_data\nWHERE title LIKE '%Manager%'\nGROUP BY gender;"
    },
    {
      "Prompt": "To analyze employee engagement trends, write a SQL query that calculates the average engagement score for each department over the last two years.",
      "Response": "SELECT department_type, AVG(engagement_score) AS avg_engagement\nFROM employee_engagement_survey_data e\nJOIN employee_data d ON e.employee_id = d.employee_id\nWHERE e.survey_date >= date('now', '-2 years')\nGROUP BY department_type;"
    },
    {
      "Prompt": "To evaluate training program outcomes, write a SQL query that calculates the completion rate and average cost of training programs grouped by training type.",
      "Response": "SELECT training_type, \n           COUNT(CASE WHEN training_outcome = 'Completed' THEN 1 END) * 100.0 / COUNT(*) AS completion_rate,\n           AVG(training_cost) AS avg_cost\nFROM training_and_development_data\nGROUP BY training_type;"
    },
    {
      "Prompt": "To understand recruitment efficiency, write a SQL query that calculates the average time to hire for selected applicants grouped by job title.",
      "Response": "SELECT job_title, \n           AVG(julianday(selection_date) - julianday(application_date)) AS avg_time_to_hire\nFROM recruitment_data\nWHERE status = 'Selected'\nGROUP BY job_title;"
    },
    {
      "Prompt": "To assess employee distribution, write a SQL query that calculates the number of employees in each business unit and their average years of service.",
      "Response": "SELECT business_unit, COUNT(*) AS employee_count, \n           AVG(julianday('now') - julianday(start_date)) / 365.0 AS avg_years_of_service\nFROM employee_data\nGROUP BY business_unit;"
    },
    {
      "Prompt": "To analyze performance trends, write a SQL query that calculates the average performance score for each department and filters for departments with an average score above 85.",
      "Response": "SELECT department_type, AVG(performance_score) AS avg_performance\nFROM employee_data\nGROUP BY department_type\nHAVING avg_performance > 85;"
    },
    {
      "Prompt": "To understand training participation, write a SQL query that calculates the percentage of employees in each department who attended at least one training program.",
      "Response": "SELECT d.department_type, \n           COUNT(DISTINCT t.employee_id) * 100.0 / COUNT(DISTINCT d.employee_id) AS participation_rate\nFROM employee_data d\nLEFT JOIN training_and_development_data t ON d.employee_id = t.employee_id\nGROUP BY d.department_type;"
    },
    {
      "Prompt": "To analyze hiring trends, write a SQL query that calculates the number of applications received monthly for each job title over the past year.",
      "Response": "SELECT strftime('%Y-%m', application_date) AS application_month, job_title, COUNT(*) AS application_count\nFROM recruitment_data\nWHERE application_date >= date('now', '-1 year')\nGROUP BY application_month, job_title;"
    },
    {
      "Prompt": "To evaluate gender diversity in management roles, write a SQL query that calculates the percentage of male and female employees in managerial positions.",
      "Response": "SELECT gender, \n           COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage\nFROM employee_data\nWHERE title LIKE '%Manager%'\nGROUP BY gender;"
    },
    {
      "Prompt": "To assess training cost efficiency, write a SQL query that calculates the total cost and average cost per attendee for each training program.",
      "Response": "SELECT training_program_name, \n           SUM(training_cost) AS total_cost,\n           SUM(training_cost) / COUNT(employee_id) AS avg_cost_per_attendee\nFROM training_and_development_data\nGROUP BY training_program_name;"
    },
    {
      "Prompt": "To update the department of employees based on recent role changes, write a SQL query that updates the department of employees with the title 'Team Lead'.",
      "Response": "UPDATE employee_data\nSET department_type = 'Leadership'\nWHERE title = 'Team Lead';"
    },
    {
      "Prompt": "To clean up records, write a SQL query that deletes employees who have been inactive for more than 3 years.",
      "Response": "DELETE FROM employee_data\nWHERE employee_status = 'Inactive' AND julianday('now') - julianday(exit_date) > 3 * 365;"
    },
    {
      "Prompt": "To reward outstanding employees, write a SQL query that inserts a bonus record for employees with performance scores greater than 90.",
      "Response": "INSERT INTO bonuses (employee_id, bonus_amount, bonus_date)\nSELECT employee_id, 1000, date('now')\nFROM employee_data\nWHERE performance_score > 90;"
    },
    {
      "Prompt": "To update training records, write a SQL query that updates the training status of employees who have completed their programs.",
      "Response": "UPDATE training_and_development_data\nSET training_outcome = 'Completed'\nWHERE training_date <= date('now', '-1 month');"
    },
    {
      "Prompt": "To remove duplicate recruitment entries, write a SQL query that deletes duplicate applicants based on email and job title.",
      "Response": "DELETE FROM recruitment_data\nWHERE rowid NOT IN (\n    SELECT MIN(rowid)\n    FROM recruitment_data\n    GROUP BY email, job_title\n);"
    },
    {
      "Prompt": "To add training feedback records, write a SQL query that inserts feedback for employees who completed the 'Leadership Skills' training.",
      "Response": "INSERT INTO training_feedback (employee_id, training_program_name, feedback_date, feedback_score)\nSELECT employee_id, training_program_name, date('now'), NULL\nFROM training_and_development_data\nWHERE training_program_name = 'Leadership Skills' AND training_outcome = 'Completed';"
    },
    {
      "Prompt": "To update job titles for accuracy, write a SQL query that appends 'Junior' to the title of employees hired less than 2 years ago.",
      "Response": "UPDATE employee_data\nSET title = 'Junior ' || title\nWHERE julianday('now') - julianday(start_date) < 2 * 365;"
    },
    {
      "Prompt": "To manage training schedules, write a SQL query that deletes training records older than 5 years.",
      "Response": "DELETE FROM training_and_development_data\nWHERE julianday('now') - julianday(training_date) > 5 * 365;"
    },
    {
      "Prompt": "To insert new hires into the employee database, write a SQL query that adds employees from a temporary table who are not already in the main table.",
      "Response": "INSERT INTO employee_data (employee_id, first_name, last_name, title, start_date)\nSELECT temp_id, temp_first_name, temp_last_name, temp_title, temp_start_date\nFROM temp_employees\nWHERE temp_id NOT IN (SELECT employee_id FROM employee_data);"
    },
    {
      "Prompt": "To update salary bands, write a SQL query that increases the pay zone by one level for employees in management roles.",
      "Response": "UPDATE employee_data\nSET pay_zone = pay_zone + 1\nWHERE title LIKE '%Manager%';"
    },
    {
      "Prompt": "To clear outdated survey data, write a SQL query that deletes survey responses older than 3 years.",
      "Response": "DELETE FROM employee_engagement_survey_data\nWHERE julianday('now') - julianday(survey_date) > 3 * 365;"
    },
    {
      "Prompt": "To reward employees who completed high-cost training programs, write a SQL query that inserts reward records into a table for those programs over $5000.",
      "Response": "INSERT INTO training_rewards (employee_id, training_program_name, reward_date)\nSELECT employee_id, training_program_name, date('now')\nFROM training_and_development_data\nWHERE training_cost > 5000 AND training_outcome = 'Completed';"
    },
    {
      "Prompt": "To standardize job titles, write a SQL query that replaces 'Software Engineer' with 'Developer' across all records.",
      "Response": "UPDATE employee_data\nSET title = REPLACE(title, 'Software Engineer', 'Developer');"
    },
    {
      "Prompt": "To clean up terminated employees' training data, write a SQL query that deletes training records for employees no longer active.",
      "Response": "DELETE FROM training_and_development_data\nWHERE employee_id IN (\n    SELECT employee_id\n    FROM employee_data\n    WHERE employee_status = 'Terminated'\n);"
    },
    {
      "Prompt": "To promote employees with exceptional performance, write a SQL query that updates their title to 'Senior' followed by their current title.",
      "Response": "UPDATE employee_data\nSET title = 'Senior ' || title\nWHERE performance_score > 90;"
    },
    {
      "Prompt": "To insert performance review data, write a SQL query that adds a review for employees with no existing reviews in the current year.",
      "Response": "INSERT INTO performance_reviews (employee_id, review_date, review_score)\nSELECT employee_id, date('now'), NULL\nFROM employee_data\nWHERE employee_id NOT IN (\n    SELECT employee_id\n    FROM performance_reviews\n    WHERE strftime('%Y', review_date) = strftime('%Y', 'now')\n);"
    },
    {
      "Prompt": "To manage outdated job postings, write a SQL query that deletes recruitment entries for positions unfilled for over a year.",
      "Response": "DELETE FROM recruitment_data\nWHERE status = 'Open' AND julianday('now') - julianday(application_date) > 365;"
    },
    {
      "Prompt": "To update department types for reorganization, write a SQL query that sets all 'Operations' departments to 'Business Operations'.",
      "Response": "UPDATE employee_data\nSET department_type = 'Business Operations'\nWHERE department_type = 'Operations';"
    },
    {
      "Prompt": "To insert feedback for employees attending safety training, write a SQL query that adds records to the feedback table.",
      "Response": "INSERT INTO feedback (employee_id, feedback_type, feedback_date)\nSELECT employee_id, 'Safety Training', date('now')\nFROM training_and_development_data\nWHERE training_program_name = 'Safety' AND training_outcome = 'Completed';"
    },
    {
      "Prompt": "To clean up duplicates, write a SQL query that deletes duplicate employee entries based on email and start date.",
      "Response": "DELETE FROM employee_data\nWHERE rowid NOT IN (\n    SELECT MIN(rowid)\n    FROM employee_data\n    GROUP BY email, start_date\n);"
    },
    {
      "Prompt": "To recognize employee achievements, write a SQL query that inserts award records for employees with a satisfaction score above 90.",
      "Response": "INSERT INTO awards (employee_id, award_date, award_type)\nSELECT employee_id, date('now'), 'High Satisfaction'\nFROM employee_engagement_survey_data\nWHERE satisfaction_score > 90;"
    },
    {
      "Prompt": "To adjust salary ranges, write a SQL query that updates the pay zone for employees in the 'Development' department to one level higher.",
      "Response": "UPDATE employee_data\nSET pay_zone = pay_zone + 1\nWHERE department_type = 'Development';"
    },
    {
      "Prompt": "To insert survey reminders, write a SQL query that adds reminder records for employees who have not completed a survey this year.",
      "Response": "INSERT INTO reminders (employee_id, reminder_date, reminder_type)\nSELECT employee_id, date('now'), 'Survey Reminder'\nFROM employee_data\nWHERE employee_id NOT IN (\n    SELECT employee_id\n    FROM employee_engagement_survey_data\n    WHERE strftime('%Y', survey_date) = strftime('%Y', 'now')\n);"
    },
    {
      "Prompt": "To standardize department names, write a SQL query that updates all instances of 'HR' to 'Human Resources'.",
      "Response": "UPDATE employee_data\nSET department_type = 'Human Resources'\nWHERE department_type = 'HR';"
    },
    {
      "Prompt": "To remove inactive applicants, write a SQL query that deletes recruitment records for applicants whose status is 'Rejected' for over a year.",
      "Response": "DELETE FROM recruitment_data\nWHERE status = 'Rejected' AND julianday('now') - julianday(application_date) > 365;"
    },
    {
      "Prompt": "To promote long-term employees, write a SQL query that updates their titles to 'Senior' followed by their current title for employees with over 10 years of service.",
      "Response": "UPDATE employee_data\nSET title = 'Senior ' || title\nWHERE julianday('now') - julianday(start_date) > 10 * 365;"
    },
    {
      "Prompt": "To recognize exceptional trainers, write a SQL query that inserts trainer awards for those conducting training programs with an average score above 4.5.",
      "Response": "INSERT INTO trainer_awards (trainer_name, award_date, award_type)\nSELECT trainer, date('now'), 'Excellence Award'\nFROM training_and_development_data\nWHERE training_program_name IN (\n    SELECT training_program_name\n    FROM training_feedback\n    GROUP BY training_program_name\n    HAVING AVG(feedback_score) > 4.5\n);"
    },
]

{
      "Prompt": "To analyze recruitment success, write a SQL query that calculates the selection rate for each job title.",
      "Response": "SELECT job_title, \n           COUNT(CASE WHEN status = 'Selected' THEN 1 END) * 100.0 / COUNT(*) AS selection_rate\nFROM recruitment_data\nGROUP BY job_title;"
    },
    {
      "Prompt": "To evaluate employee engagement, write a SQL query that calculates the average engagement score for each business unit and filters for units with an average score above 80.",
      "Response": "SELECT business_unit, AVG(engagement_score) AS avg_engagement\nFROM employee_engagement_survey_data e\nJOIN employee_data d ON e.employee_id = d.employee_id\nGROUP BY business_unit\nHAVING avg_engagement > 80;"
    },
    {
      "Prompt": "To understand training impact, write a SQL query that identifies employees who completed the 'Technical Skills' training and achieved a performance score above 90.",
      "Response": "SELECT d.first_name, d.last_name, d.title\nFROM training_and_development_data t\nJOIN employee_data d ON t.employee_id = d.employee_id\nWHERE t.training_program_name = 'Technical Skills' AND d.performance_score > 90;"
    },
    {
      "Prompt": "To analyze work-life balance, write a SQL query that calculates the average work-life balance score for each department.",
      "Response": "SELECT department_type, AVG(work_life_balance_score) AS avg_balance\nFROM employee_engagement_survey_data e\nJOIN employee_data d ON e.employee_id = d.employee_id\nGROUP BY department_type;"
    },
    {
      "Prompt": "To monitor exit trends, write a SQL query that counts the number of employees who exited the company each year grouped by department.",
      "Response": "SELECT strftime('%Y', exit_date) AS exit_year, department_type, COUNT(*) AS exit_count\nFROM employee_data\nWHERE exit_date IS NOT NULL\nGROUP BY exit_year, department_type;"
    },
    {
      "Prompt": "To evaluate leadership effectiveness, write a SQL query that identifies managers with a performance score below 70. Include their names, job titles, and departments.",
      "Response": "SELECT first_name, last_name, title, department_type\nFROM employee_data\nWHERE title LIKE '%Manager%' AND performance_score < 70;"
    },
    {
      "Prompt": "To analyze engagement trends, write a SQL query that calculates the yearly average engagement score for the company.",
      "Response": "SELECT strftime('%Y', survey_date) AS survey_year, AVG(engagement_score) AS avg_engagement\nFROM employee_engagement_survey_data\nGROUP BY survey_year;"
    },
    {
      "Prompt": "To understand applicant demographics, write a SQL query that calculates the average years of experience for applicants grouped by education level.",
      "Response": "SELECT education_level, AVG(years_of_experience) AS avg_experience\nFROM recruitment_data\nGROUP BY education_level;"
    },
    {
      "Prompt": "To analyze departmental satisfaction, write a SQL query that calculates the average satisfaction score for employees grouped by division.",
      "Response": "SELECT division_description, AVG(satisfaction_score) AS avg_satisfaction\nFROM employee_engagement_survey_data e\nJOIN employee_data d ON e.employee_id = d.employee_id\nGROUP BY division_description;"
    },
    {
      "Prompt": "To evaluate termination trends, write a SQL query that calculates the termination rate for each department over the last 5 years.",
      "Response": "SELECT department_type, \n           COUNT(CASE WHEN exit_date IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS termination_rate\nFROM employee_data\nWHERE julianday('now') - julianday(start_date) <= 5 * 365\nGROUP BY department_type;"
    },
    {
      "Prompt": "To assess engagement distribution, write a SQL query that calculates the percentage of employees with engagement scores in different ranges.",
      "Response": "SELECT \n    CASE \n        WHEN engagement_score < 50 THEN 'Low'\n        WHEN engagement_score BETWEEN 50 AND 80 THEN 'Medium'\n        ELSE 'High'\n    END AS engagement_range,\n    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage\nFROM employee_engagement_survey_data\nGROUP BY engagement_range;"
    },
    {
      "Prompt": "To track recruitment patterns, write a SQL query that calculates the monthly application count for each state.",
      "Response": "SELECT strftime('%Y-%m', application_date) AS application_month, state, COUNT(*) AS application_count\nFROM recruitment_data\nGROUP BY application_month, state;"
    },
    {
      "Prompt": "To evaluate pay zones, write a SQL query that calculates the average and median pay zone for employees grouped by job title.",
      "Response": "SELECT title, AVG(pay_zone) AS avg_pay_zone,\n           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pay_zone) AS median_pay_zone\nFROM employee_data\nGROUP BY title;"
    },
    {
      "Prompt": "To analyze training costs, write a SQL query that calculates the total cost and average cost per day for each training program.",
      "Response": "SELECT training_program_name, SUM(training_cost) AS total_cost,\n           AVG(training_cost / training_duration_days) AS avg_cost_per_day\nFROM training_and_development_data\nGROUP BY training_program_name;"
    },
    
