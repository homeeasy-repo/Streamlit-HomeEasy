import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def save_to_db(data):
    """
    Save client requirements to the database.

    Args:
        data (dict): A dictionary containing client requirement data.

    Returns:
        bool: True if the data was saved successfully, False otherwise.
    """
    try:
        # Connect to the database
        conn = psycopg2.connect(DB_URL, sslmode="require")
        cur = conn.cursor()

        # Insert data into the database
        query = """
            INSERT INTO client_requirements (
                client_id, move_in_date, move_in_date_max, budget, budget_max,
                beds, baths, sqft, sqft_max, parking, pets, washer_dryer,
                zip, neighborhood, amenities, comment, pets_comment,
                parking_comment, moving_reason, work_location, commuting,
                people_living, building_must_haves, unit_must_haves,
                special_needs, preference, personality, another_broker,
                another_broker_comment, confirm_tour, tour_person,
                availability, lease_term, section8, monthly_income,
                credit_score, cosigner, cosigner_comment,
                neighborhood_specific, tour_date
            ) VALUES (
                %(client_id)s, %(move_in_date)s, %(move_in_date_max)s, %(budget)s, %(budget_max)s,
                %(beds)s, %(baths)s, %(sqft)s, %(sqft_max)s, %(parking)s, %(pets)s, %(washer_dryer)s,
                %(zip)s, %(neighborhood)s, %(amenities)s, %(comment)s, %(pets_comment)s,
                %(parking_comment)s, %(moving_reason)s, %(work_location)s, %(commuting)s,
                %(people_living)s, %(building_must_haves)s, %(unit_must_haves)s,
                %(special_needs)s, %(preference)s, %(personality)s, %(another_broker)s,
                %(another_broker_comment)s, %(confirm_tour)s, %(tour_person)s,
                %(availability)s, %(lease_term)s, %(section8)s, %(monthly_income)s,
                %(credit_score)s, %(cosigner)s, %(cosigner_comment)s,
                %(neighborhood_specific)s, %(tour_date)s
            )
        """

        cur.execute(query, data)
        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error saving to database: {e}")
        return False
