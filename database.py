import sqlite3, secrets, string
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "campaign_manager.db"

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def add_campaign(name, dm_name, system, invite_code):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO campaigns (name, dm_name, system, invite_code)
    VALUES (?, ?, ?, ?)
""", (name, dm_name, system, invite_code))

    connection.commit()
    campaign_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return campaign_id

def get_campaigns():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM campaigns")
    campaigns = cursor.fetchall()

    cursor.close()
    connection.close()

    return campaigns

def get_campaign(campaign_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM campaigns
        WHERE id = ?
        """, (campaign_id, ))
    campaign = cursor.fetchone()

    cursor.close()
    connection.close()

    return campaign

def add_player(campaign_id, player_name, character_name, character_class, level, race):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO players (campaign_id, player_name, character_name, character_class, level, race)
    VALUES (?, ?, ?, ?, ?, ?)
""", (campaign_id, player_name, character_name, character_class, level, race))

    connection.commit()
    player_id = cursor.lastrowid

    cursor.close()
    connection.close()  


    return player_id

def get_players(campaign_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM players
        WHERE campaign_id = ?
    """, (campaign_id,))

    players = cursor.fetchall()

    cursor.close()
    connection.close()

    return players

def add_npc(campaign_id, npc_name, npc_class, npc_level, npc_race):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO npcs (campaign_id, npc_name, npc_class, npc_level, npc_race)
    VALUES(?, ?, ?, ?, ?)
    """, (campaign_id, npc_name, npc_class, npc_level, npc_race))

    connection.commit()
    npc_id = cursor.lastrowid

    cursor.close()
    connection.close()  

    return npc_id

def get_npcs(campaign_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM npcs
        WHERE campaign_id = ?
    """, (campaign_id,))

    npcs = cursor.fetchall()

    cursor.close()
    connection.close()

    return npcs

def add_location(campaign_id, location_name, location_type, location_region, location_description):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO locations (campaign_id, location_name, location_type, location_region, location_description)
    VALUES(?, ?, ?, ?, ?)
    """, (campaign_id, location_name, location_type, location_region, location_description))

    connection.commit()
    location_id = cursor.lastrowid

    cursor.close()
    connection.close()  

    return location_id

def get_locations(campaign_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM locations
        WHERE campaign_id = ?
    """, (campaign_id,))

    locations = cursor.fetchall()

    cursor.close()
    connection.close()

    return locations

def add_note(campaign_id, note_title, note_category, note_content, note_visibility):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO notes (campaign_id, note_title, note_category, note_content, note_visibility)
    VALUES(?, ?, ?, ?, ?)
    """, (campaign_id, note_title, note_category, note_content, note_visibility))

    connection.commit()
    note_id = cursor.lastrowid

    cursor.close()
    connection.close()  

    return note_id

def get_notes(campaign_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM notes
        WHERE campaign_id = ?
    """, (campaign_id,))

    notes = cursor.fetchall()

    cursor.close()
    connection.close()

    return notes

def delete_player(player_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM players
        where id = ?
    """, (player_id,))

    connection.commit()

    cursor.close()
    connection.close()

def delete_npc(npc_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM npcs
        where id = ?
    """, (npc_id,))

    connection.commit()

    cursor.close()
    connection.close()

def delete_location(location_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM locations
        where id = ?
    """, (location_id,))

    connection.commit()

    cursor.close()
    connection.close()

def delete_note(note_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM notes
        where id = ?
    """, (note_id,))

    connection.commit()

    cursor.close()
    connection.close()

def update_player(player_id, player_name, character_name, character_class, level, race):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE players
        SET player_name = ?,
            character_name = ?,
            character_class = ?,
            level = ?,
            race = ?
        WHERE id = ?
    """, (player_name, character_name, character_class, level, race, player_id))

    connection.commit()

    cursor.close()
    connection.close()

def update_npc(npc_id, npc_name, npc_class, npc_level, npc_race):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE npcs
        SET npc_name = ?,
            npc_class = ?,
            npc_level = ?,
            npc_race = ?
        WHERE id = ?
    """, (npc_name, npc_class, npc_level, npc_race, npc_id))

    connection.commit()

    cursor.close()
    connection.close()

def update_location(location_id, location_name, location_type, location_region, location_description):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE locations
        SET location_name = ?,
            location_type = ?,
            location_region = ?,
            location_description = ?
        WHERE id = ?
    """, (location_name, location_type, location_region, location_description, location_id))

    connection.commit()

    cursor.close()
    connection.close()

def update_note(note_id, note_title, note_category, note_content, note_visibility):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE notes
        SET note_title = ?,
            note_category = ?,
            note_content = ?,
            note_visibility = ?
        WHERE id = ?
    """, (note_title, note_category, note_content, note_visibility, note_id))

    connection.commit()

    cursor.close()
    connection.close()

def get_user_by_id(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user

def add_user(email, display_name, avatar_url=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO users (email, display_name, avatar_url)
    VALUES (?, ?, ?)
""", (email, display_name, avatar_url))

    connection.commit()
    user_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return user_id

def get_auth_account(provider, provider_user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM auth_accounts
        WHERE provider = ?
        AND provider_user_id = ?
    """, (provider, provider_user_id))

    auth_account = cursor.fetchone()

    cursor.close()
    connection.close()

    return auth_account

def add_auth_account(user_id, provider, provider_user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO auth_accounts (user_id, provider, provider_user_id)
    VALUES (?, ?, ?)
""", (user_id, provider, provider_user_id))

    connection.commit()
    auth_account_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return auth_account_id

def add_campaign_member(campaign_id, user_id, role):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO campaign_members (campaign_id, user_id, role)
    VALUES (?, ?, ?)
""", (campaign_id, user_id, role))

    connection.commit()
    campaign_member_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return campaign_member_id

def get_campaigns_for_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT campaigns.*, campaign_members.role
        FROM campaigns
        JOIN campaign_members
        ON campaigns.id = campaign_members.campaign_id
        WHERE campaign_members.user_id = ?
        """, (user_id,))
    campaigns = cursor.fetchall()

    cursor.close()
    connection.close()

    return campaigns

def is_campaign_member(campaign_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM campaign_members
        WHERE campaign_id = ?
        AND user_id = ?
        """, (campaign_id, user_id))

    membership = cursor.fetchone()

    cursor.close()
    connection.close()

    if membership is not None:
        return True

    else:
        return False

def get_campaign_by_invite_code(invite_code):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM campaigns
        WHERE invite_code = ?
        """, (invite_code,))

    campaign = cursor.fetchone()

    cursor.close()
    connection.close()

    return campaign

def add_character(campaign_id, user_id, character_name, race, character_class, level, status):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO characters (campaign_id, user_id, character_name, race, character_class, level, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (campaign_id, user_id, character_name, race, character_class, level, status))

    connection.commit()
    character_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return character_id

def get_characters_for_user(campaign_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM characters
        WHERE campaign_id = ?
        AND user_id = ?
        """, (campaign_id, user_id))

    characters = cursor.fetchall()

    cursor.close()
    connection.close()

    return characters

def get_active_character(campaign_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM characters
        WHERE campaign_id = ?
        AND user_id = ?
        AND status = ?
        """, (campaign_id, user_id, "ACTIVE"))
    
    character = cursor.fetchone()

    cursor.close()
    connection.close()

    return character

def update_character_status(character_id, status):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE characters
        SET status = ?
        WHERE id = ?
    """, (status, character_id))

    connection.commit()

    cursor.close()
    connection.close()

def get_character(character_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM characters
        WHERE id = ?
    """, (character_id,))

    character = cursor.fetchone()

    cursor.close()
    connection.close()

    return character

def generate_invite_code():
    invite_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range (6))
    return invite_code

def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Campaign creation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dm_name TEXT NOT NULL,
            system TEXT NOT NULL,
            invite_code TEXT NULL
        )
    """)

    # Player creation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER NOT NULL,
        player_name TEXT NOT NULL,
        character_name TEXT NOT NULL,
        character_class TEXT NOT NULL,
        level INTEGER NOT NULL,
        race TEXT NOT NULL,
        
        FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )

    """)

    # NPC creation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS npcs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER NOT NULL,
        npc_name TEXT NOT NULL,
        npc_class TEXT NOT NULL,
        npc_level INTEGER NOT NULL,
        npc_race TEXT NOT NULL,
        
        FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )

    """)

    # Location Creation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER NOT NULL,
        location_name TEXT NOT NULL,
        location_type TEXT NOT NULL,
        location_region TEXT NOT NULL,
        location_description TEXT NOT NULL,
        
        FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )

    """)

    # Note creation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER NOT NULL,
        note_title TEXT NOT NULL,
        note_category TEXT NOT NULL,
        note_content TEXT NOT NULL,
        note_visibility TEXT NOT NULL,
        
        FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )

    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        display_name TEXT NOT NULL,
        avatar_url TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        provider TEXT NOT NULL,
        provider_user_id TEXT NOT NULL,

        FOREIGN KEY (user_id) REFERENCES users(id),
        UNIQUE (provider, provider_user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaign_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,

        FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        UNIQUE (campaign_id, user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        character_name TEXT NOT NULL,
        race TEXT NOT NULL,
        character_class TEXT NOT NULL,
        level INTEGER NOT NULL,
        status TEXT NOT NULL,
        
        FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    connection.commit()

    cursor.close()
    connection.close()

initialize_database()


