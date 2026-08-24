import sqlite3
from datetime import date, timedelta

DB_NAME = "humanitarian_supply_chain.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aid_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            warehouse TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            minimum_stock INTEGER NOT NULL,
            unit TEXT NOT NULL,
            updated_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shipment_code TEXT NOT NULL,
            item_name TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            dispatch_date TEXT NOT NULL,
            expected_date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS distributions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            distribution_date TEXT NOT NULL,
            district TEXT NOT NULL,
            distribution_center TEXT NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            households_reached INTEGER NOT NULL,
            beneficiaries_reached INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def seed_data():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM aid_inventory"
    )

    inventory_count = cursor.fetchone()[0]

    if inventory_count == 0:

        inventory_data = [
            (
                "Rice",
                "Food",
                "Central Warehouse",
                18500,
                5000,
                "kg",
                "2026-08-01"
            ),
            (
                "Lentils",
                "Food",
                "Central Warehouse",
                6200,
                2000,
                "kg",
                "2026-08-03"
            ),
            (
                "Water Purification Tablets",
                "WASH",
                "Barishal Warehouse",
                12000,
                5000,
                "tablets",
                "2026-08-05"
            ),
            (
                "Hygiene Kits",
                "WASH",
                "Barishal Warehouse",
                850,
                1000,
                "kits",
                "2026-08-07"
            ),
            (
                "Blankets",
                "Shelter",
                "Central Warehouse",
                2400,
                800,
                "pieces",
                "2026-08-06"
            ),
            (
                "Tarpaulins",
                "Shelter",
                "Khulna Warehouse",
                720,
                900,
                "pieces",
                "2026-08-09"
            ),
            (
                "Medical Kits",
                "Health",
                "Central Warehouse",
                420,
                150,
                "kits",
                "2026-08-10"
            ),
            (
                "School Kits",
                "Education",
                "Khulna Warehouse",
                1100,
                500,
                "kits",
                "2026-08-11"
            )
        ]

        cursor.executemany("""
            INSERT INTO aid_inventory (
                item_name,
                category,
                warehouse,
                quantity,
                minimum_stock,
                unit,
                updated_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, inventory_data)

    cursor.execute(
        "SELECT COUNT(*) FROM shipments"
    )

    shipment_count = cursor.fetchone()[0]

    if shipment_count == 0:

        today = date.today()

        shipment_data = [
            (
                "SHP-1001",
                "Rice",
                "Dhaka Warehouse",
                "Barishal Distribution Hub",
                5000,
                str(today - timedelta(days=4)),
                str(today - timedelta(days=1)),
                "Delivered"
            ),
            (
                "SHP-1002",
                "Hygiene Kits",
                "Dhaka Warehouse",
                "Barishal Distribution Hub",
                600,
                str(today - timedelta(days=2)),
                str(today + timedelta(days=1)),
                "In Transit"
            ),
            (
                "SHP-1003",
                "Medical Kits",
                "Dhaka Warehouse",
                "Khulna Distribution Hub",
                200,
                str(today - timedelta(days=1)),
                str(today + timedelta(days=2)),
                "In Transit"
            ),
            (
                "SHP-1004",
                "Tarpaulins",
                "Khulna Warehouse",
                "Satkhira Distribution Center",
                500,
                str(today - timedelta(days=6)),
                str(today - timedelta(days=3)),
                "Delivered"
            ),
            (
                "SHP-1005",
                "Water Purification Tablets",
                "Barishal Warehouse",
                "Patuakhali Distribution Center",
                4000,
                str(today),
                str(today + timedelta(days=3)),
                "Dispatched"
            ),
            (
                "SHP-1006",
                "School Kits",
                "Khulna Warehouse",
                "Bagerhat Distribution Center",
                700,
                str(today - timedelta(days=3)),
                str(today),
                "Delivered"
            )
        ]

        cursor.executemany("""
            INSERT INTO shipments (
                shipment_code,
                item_name,
                origin,
                destination,
                quantity,
                dispatch_date,
                expected_date,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, shipment_data)

    cursor.execute(
        "SELECT COUNT(*) FROM distributions"
    )

    distribution_count = cursor.fetchone()[0]

    if distribution_count == 0:

        distribution_data = [
            (
                "2026-08-05",
                "Barishal",
                "Barishal Sadar Center",
                "Rice",
                3200,
                640,
                2450
            ),
            (
                "2026-08-07",
                "Patuakhali",
                "Patuakhali Central Center",
                "Rice",
                2800,
                560,
                2180
            ),
            (
                "2026-08-09",
                "Satkhira",
                "Satkhira Relief Center",
                "Tarpaulins",
                350,
                350,
                1450
            ),
            (
                "2026-08-10",
                "Khulna",
                "Khulna City Center",
                "Medical Kits",
                120,
                120,
                680
            ),
            (
                "2026-08-12",
                "Bagerhat",
                "Bagerhat Distribution Center",
                "School Kits",
                500,
                500,
                1250
            ),
            (
                "2026-08-14",
                "Barishal",
                "Barishal Sadar Center",
                "Hygiene Kits",
                300,
                300,
                1100
            )
        ]

        cursor.executemany("""
            INSERT INTO distributions (
                distribution_date,
                district,
                distribution_center,
                item_name,
                quantity,
                households_reached,
                beneficiaries_reached
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, distribution_data)

    conn.commit()
    conn.close()


def get_inventory():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id,
            item_name,
            category,
            warehouse,
            quantity,
            minimum_stock,
            unit,
            updated_date
        FROM aid_inventory
        ORDER BY item_name
    """).fetchall()

    conn.close()

    return rows


def get_shipments():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id,
            shipment_code,
            item_name,
            origin,
            destination,
            quantity,
            dispatch_date,
            expected_date,
            status
        FROM shipments
        ORDER BY dispatch_date DESC
    """).fetchall()

    conn.close()

    return rows


def get_distributions():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id,
            distribution_date,
            district,
            distribution_center,
            item_name,
            quantity,
            households_reached,
            beneficiaries_reached
        FROM distributions
        ORDER BY distribution_date DESC
    """).fetchall()

    conn.close()

    return rows


def add_inventory(
    item_name,
    category,
    warehouse,
    quantity,
    minimum_stock,
    unit
):

    conn = get_connection()

    conn.execute("""
        INSERT INTO aid_inventory (
            item_name,
            category,
            warehouse,
            quantity,
            minimum_stock,
            unit,
            updated_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        item_name,
        category,
        warehouse,
        quantity,
        minimum_stock,
        unit,
        str(date.today())
    ))

    conn.commit()
    conn.close()


def add_shipment(
    shipment_code,
    item_name,
    origin,
    destination,
    quantity,
    dispatch_date,
    expected_date,
    status
):

    conn = get_connection()

    conn.execute("""
        INSERT INTO shipments (
            shipment_code,
            item_name,
            origin,
            destination,
            quantity,
            dispatch_date,
            expected_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        shipment_code,
        item_name,
        origin,
        destination,
        quantity,
        dispatch_date,
        expected_date,
        status
    ))

    conn.commit()
    conn.close()


def add_distribution(
    distribution_date,
    district,
    distribution_center,
    item_name,
    quantity,
    households_reached,
    beneficiaries_reached
):

    conn = get_connection()

    conn.execute("""
        INSERT INTO distributions (
            distribution_date,
            district,
            distribution_center,
            item_name,
            quantity,
            households_reached,
            beneficiaries_reached
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        distribution_date,
        district,
        distribution_center,
        item_name,
        quantity,
        households_reached,
        beneficiaries_reached
    ))

    conn.commit()
    conn.close()