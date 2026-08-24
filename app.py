import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database import (
    initialize_database,
    seed_data,
    get_inventory,
    get_shipments,
    get_distributions,
    add_inventory,
    add_shipment,
    add_distribution,
)

st.set_page_config(
    page_title="Humanitarian Supply Chain Analytics",
    page_icon="🌍",
    layout="wide",
)

initialize_database()
seed_data()

st.title("🌍 Humanitarian Supply Chain & Aid Distribution Analytics")
st.caption(
    "Data-driven monitoring of humanitarian inventory, shipments, "
    "distribution and supply gaps."
)

inventory_columns = [
    "ID",
    "Item",
    "Category",
    "Warehouse",
    "Quantity",
    "Minimum Stock",
    "Unit",
    "Updated Date",
]

shipment_columns = [
    "ID",
    "Shipment Code",
    "Item",
    "Origin",
    "Destination",
    "Quantity",
    "Dispatch Date",
    "Expected Date",
    "Status",
]

distribution_columns = [
    "ID",
    "Date",
    "District",
    "Distribution Center",
    "Item",
    "Quantity",
    "Households Reached",
    "Beneficiaries Reached",
]


def load_inventory():
    return pd.DataFrame(get_inventory(), columns=inventory_columns)


def load_shipments():
    return pd.DataFrame(get_shipments(), columns=shipment_columns)


def load_distributions():
    return pd.DataFrame(get_distributions(), columns=distribution_columns)


inventory_df = load_inventory()
shipments_df = load_shipments()
distributions_df = load_distributions()

inventory_df["Stock Gap"] = (
    inventory_df["Minimum Stock"] - inventory_df["Quantity"]
).clip(lower=0)

inventory_df["Stock Status"] = inventory_df.apply(
    lambda row: "⚠️ Low Stock"
    if row["Quantity"] < row["Minimum Stock"]
    else "✅ Sufficient",
    axis=1,
)

total_inventory_items = len(inventory_df)
total_inventory_quantity = int(inventory_df["Quantity"].sum())
low_stock_items = int(
    (inventory_df["Quantity"] < inventory_df["Minimum Stock"]).sum()
)

total_shipments = len(shipments_df)
in_transit = int(
    shipments_df["Status"].isin(["In Transit", "Dispatched"]).sum()
)

delivered_shipments = int(
    (shipments_df["Status"] == "Delivered").sum()
)

total_beneficiaries = int(
    distributions_df["Beneficiaries Reached"].sum()
)

total_households = int(
    distributions_df["Households Reached"].sum()
)

total_distributed = int(
    distributions_df["Quantity"].sum()
)


st.sidebar.title("🌍 Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Inventory",
        "Shipment Tracking",
        "Distribution Monitoring",
        "Reports",
    ],
)


if page == "Dashboard":

    st.subheader("📊 Humanitarian Supply Chain Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Inventory Items",
        total_inventory_items,
    )

    col2.metric(
        "Low Stock Items",
        low_stock_items,
    )

    col3.metric(
        "Active Shipments",
        in_transit,
    )

    col4.metric(
        "Beneficiaries Reached",
        f"{total_beneficiaries:,}",
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        category_summary = (
            inventory_df
            .groupby("Category")["Quantity"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            category_summary,
            x="Category",
            y="Quantity",
            title="Inventory by Aid Category",
            text_auto=True,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with right:

        shipment_summary = (
            shipments_df["Status"]
            .value_counts()
            .reset_index()
        )

        shipment_summary.columns = [
            "Status",
            "Count",
        ]

        fig = px.pie(
            shipment_summary,
            names="Status",
            values="Count",
            title="Shipment Status",
            hole=0.4,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.subheader("⚠️ Supply Gap Monitoring")

    low_stock_df = inventory_df[
        inventory_df["Quantity"] < inventory_df["Minimum Stock"]
    ].copy()

    if low_stock_df.empty:

        st.success(
            "No critical inventory shortages detected."
        )

    else:

        st.warning(
            f"{len(low_stock_df)} item(s) are below minimum stock level."
        )

        st.dataframe(
            low_stock_df[
                [
                    "Item",
                    "Category",
                    "Warehouse",
                    "Quantity",
                    "Minimum Stock",
                    "Stock Gap",
                    "Unit",
                    "Stock Status",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    st.subheader("📦 Recent Shipments")

    st.dataframe(
        shipments_df.head(5),
        use_container_width=True,
        hide_index=True,
    )


elif page == "Inventory":

    st.subheader("📦 Aid Inventory Management")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Inventory Quantity",
        f"{total_inventory_quantity:,}",
    )

    col2.metric(
        "Inventory Categories",
        inventory_df["Category"].nunique(),
    )

    col3.metric(
        "Low Stock Items",
        low_stock_items,
    )

    st.divider()

    st.dataframe(
        inventory_df,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("➕ Add Inventory")

    with st.form("inventory_form"):

        c1, c2, c3 = st.columns(3)

        item_name = c1.text_input(
            "Item Name"
        )

        category = c2.selectbox(
            "Category",
            [
                "Food",
                "WASH",
                "Shelter",
                "Health",
                "Education",
            ],
        )

        warehouse = c3.text_input(
            "Warehouse"
        )

        c4, c5, c6 = st.columns(3)

        quantity = c4.number_input(
            "Quantity",
            min_value=0,
            step=1,
        )

        minimum_stock = c5.number_input(
            "Minimum Stock",
            min_value=0,
            step=1,
        )

        unit = c6.text_input(
            "Unit",
            value="units",
        )

        submitted = st.form_submit_button(
            "Add Inventory"
        )

        if submitted:

            if (
                item_name.strip()
                and warehouse.strip()
                and unit.strip()
            ):

                add_inventory(
                    item_name.strip(),
                    category,
                    warehouse.strip(),
                    int(quantity),
                    int(minimum_stock),
                    unit.strip(),
                )

                st.success(
                    "Inventory item added successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Please complete all required fields."
                )


elif page == "Shipment Tracking":

    st.subheader("🚚 Shipment Tracking")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Shipments",
        total_shipments,
    )

    col2.metric(
        "In Transit",
        in_transit,
    )

    col3.metric(
        "Delivered",
        delivered_shipments,
    )

    st.divider()

    status_filter = st.selectbox(
        "Filter by Status",
        [
            "All",
            "Delivered",
            "In Transit",
            "Dispatched",
        ],
    )

    filtered_shipments = shipments_df.copy()

    if status_filter != "All":

        filtered_shipments = filtered_shipments[
            filtered_shipments["Status"]
            == status_filter
        ]

    st.dataframe(
        filtered_shipments,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("➕ Add Shipment")

    with st.form("shipment_form"):

        c1, c2, c3 = st.columns(3)

        shipment_code = c1.text_input(
            "Shipment Code"
        )

        item_name = c2.text_input(
            "Item Name"
        )

        quantity = c3.number_input(
            "Quantity",
            min_value=1,
            step=1,
        )

        c4, c5 = st.columns(2)

        origin = c4.text_input(
            "Origin"
        )

        destination = c5.text_input(
            "Destination"
        )

        c6, c7, c8 = st.columns(3)

        dispatch_date = c6.date_input(
            "Dispatch Date",
            value=date.today(),
        )

        expected_date = c7.date_input(
            "Expected Delivery Date",
            value=date.today(),
        )

        status = c8.selectbox(
            "Status",
            [
                "Dispatched",
                "In Transit",
                "Delivered",
            ],
        )

        submitted = st.form_submit_button(
            "Add Shipment"
        )

        if submitted:

            if (
                shipment_code.strip()
                and item_name.strip()
                and origin.strip()
                and destination.strip()
            ):

                add_shipment(
                    shipment_code.strip(),
                    item_name.strip(),
                    origin.strip(),
                    destination.strip(),
                    int(quantity),
                    str(dispatch_date),
                    str(expected_date),
                    status,
                )

                st.success(
                    "Shipment added successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Please complete all required fields."
                )


elif page == "Distribution Monitoring":

    st.subheader("📍 Distribution Monitoring")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Households Reached",
        f"{total_households:,}",
    )

    col2.metric(
        "Beneficiaries Reached",
        f"{total_beneficiaries:,}",
    )

    col3.metric(
        "Items Distributed",
        f"{total_distributed:,}",
    )

    st.divider()

    district_summary = (
        distributions_df
        .groupby("District")
        .agg(
            Beneficiaries=(
                "Beneficiaries Reached",
                "sum",
            ),
            Households=(
                "Households Reached",
                "sum",
            ),
            Quantity=(
                "Quantity",
                "sum",
            ),
        )
        .reset_index()
    )

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            district_summary,
            x="District",
            y="Beneficiaries",
            title="Beneficiaries Reached by District",
            text_auto=True,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with right:

        fig = px.bar(
            district_summary,
            x="District",
            y="Quantity",
            title="Distributed Quantity by District",
            text_auto=True,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.subheader("Distribution Records")

    st.dataframe(
        distributions_df,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("➕ Add Distribution Record")

    with st.form("distribution_form"):

        c1, c2, c3 = st.columns(3)

        distribution_date = c1.date_input(
            "Distribution Date",
            value=date.today(),
        )

        district = c2.text_input(
            "District"
        )

        distribution_center = c3.text_input(
            "Distribution Center"
        )

        c4, c5, c6, c7 = st.columns(4)

        item_name = c4.text_input(
            "Item Name"
        )

        quantity = c5.number_input(
            "Quantity",
            min_value=1,
            step=1,
        )

        households_reached = c6.number_input(
            "Households Reached",
            min_value=0,
            step=1,
        )

        beneficiaries_reached = c7.number_input(
            "Beneficiaries Reached",
            min_value=0,
            step=1,
        )

        submitted = st.form_submit_button(
            "Add Distribution"
        )

        if submitted:

            if (
                district.strip()
                and distribution_center.strip()
                and item_name.strip()
            ):

                add_distribution(
                    str(distribution_date),
                    district.strip(),
                    distribution_center.strip(),
                    item_name.strip(),
                    int(quantity),
                    int(households_reached),
                    int(beneficiaries_reached),
                )

                st.success(
                    "Distribution record added successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Please complete all required fields."
                )


elif page == "Reports":

    st.subheader("📑 Humanitarian Supply Chain Reports")

    report_type = st.selectbox(
        "Select Report",
        [
            "Inventory Report",
            "Shipment Report",
            "Distribution Report",
            "District Performance",
        ],
    )

    if report_type == "Inventory Report":

        report_df = inventory_df.copy()

        st.dataframe(
            report_df,
            use_container_width=True,
            hide_index=True,
        )

    elif report_type == "Shipment Report":

        report_df = shipments_df.copy()

        st.dataframe(
            report_df,
            use_container_width=True,
            hide_index=True,
        )

    elif report_type == "Distribution Report":

        report_df = distributions_df.copy()

        st.dataframe(
            report_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        report_df = (
            distributions_df
            .groupby("District")
            .agg(
                Households_Reached=(
                    "Households Reached",
                    "sum",
                ),
                Beneficiaries_Reached=(
                    "Beneficiaries Reached",
                    "sum",
                ),
                Distributed_Quantity=(
                    "Quantity",
                    "sum",
                ),
            )
            .reset_index()
        )

        st.dataframe(
            report_df,
            use_container_width=True,
            hide_index=True,
        )

    csv_data = report_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Report CSV",
        data=csv_data,
        file_name=(
            report_type.lower()
            .replace(" ", "_")
            + ".csv"
        ),
        mime="text/csv",
    )

st.sidebar.divider()

st.sidebar.caption(
    "Humanitarian Supply Chain Analytics"
)

st.sidebar.caption(
    "Portfolio project using synthetic data."
)