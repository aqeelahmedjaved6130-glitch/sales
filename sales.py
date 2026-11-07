import streamlit as st
import pandas as pd
from datetime import datetime

# Page Setup (Optimized for Mobile and Desktop)
st.set_page_config(page_title="Inventory & Billing System", layout="wide")

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "current_salesman" not in st.session_state:
    st.session_state.current_salesman = ""
if "invoices_history" not in st.session_state:
    st.session_state.invoices_history = []

if "inventory" not in st.session_state:
    initial_data = [
        # Light Truck Section
        {"ID": "LT-01", "Category": "Light Truck", "Name": "4.50-12 DIAMOND JUNOON (TYRE & TUBE)", "Cost Rate": 5677.97, "Sale Rate": 6700.0, "Stock": 20},
        {"ID": "LT-02", "Category": "Light Truck", "Name": "4.50-12 DIAMOND COMMANDER (TYRE & TUBE)", "Cost Rate": 5762.71, "Sale Rate": 6800.0, "Stock": 15},
        {"ID": "LT-03", "Category": "Light Truck", "Name": "5.00-10 DIAMOND MARSHAL (TYRE & TUBE)", "Cost Rate": 5805.08, "Sale Rate": 6850.0, "Stock": 10},
        {"ID": "LT-04", "Category": "Light Truck", "Name": "5.00-12 DIAMOND THUNDER (TYRE & TUBE)", "Cost Rate": 6919.49, "Sale Rate": 8165.0, "Stock": 25},
        {"ID": "LT-11", "Category": "Light Truck", "Name": "6.50-14 DIAMOND COMMANDER (TYRE & TUBE)", "Cost Rate": 18834.75, "Sale Rate": 22225.0, "Stock": 8},
        
        # Agriculture Section
        {"ID": "AG-01", "Category": "Agriculture", "Name": "6.00-16 DIAMOND DHOOM (6 PR)", "Cost Rate": 9203.39, "Sale Rate": 10860.0, "Stock": 12},
        {"ID": "AG-04", "Category": "Agriculture", "Name": "6.00-16 CG DIAMOND THUNDER (10 PR)", "Cost Rate": 10233.05, "Sale Rate": 12075.0, "Stock": 6},
        {"ID": "AG-05", "Category": "Agriculture", "Name": "7.50-16 DIAMOND DHOOM (8 PR)", "Cost Rate": 15169.49, "Sale Rate": 17900.0, "Stock": 10},
        
        # Three Wheeler Section
        {"ID": "3W-01", "Category": "Three Wheeler", "Name": "4.00-8 F DIAMOND COMMANDER (8 PR)", "Cost Rate": 3555.08, "Sale Rate": 4195.0, "Stock": 30},
        {"ID": "3W-08", "Category": "Three Wheeler", "Name": "4.00-8 R DIAMOND THUNDER (10 PR)", "Cost Rate": 3843.22, "Sale Rate": 4535.0, "Stock": 40},
        {"ID": "3W-10", "Category": "Three Wheeler", "Name": "1.35-10 DIAMOND ROCK STAR (10 PR)", "Cost Rate": 4716.10, "Sale Rate": 5565.0, "Stock": 15},
        
        # Motor Cycle Section
        {"ID": "MC-01", "Category": "Motor Cycle", "Name": "2.25-17 FRONT EXTREME (4PR)", "Cost Rate": 2093.22, "Sale Rate": 2470.0, "Stock": 50},
        {"ID": "MC-05", "Category": "Motor Cycle", "Name": "2.50-17 FRONT JUMBO (6PR)", "Cost Rate": 2360.17, "Sale Rate": 2785.0, "Stock": 45},
        {"ID": "MC-40", "Category": "Motor Cycle", "Name": "2.75-18 REAR ALTIS (6PR)", "Cost Rate": 3245.76, "Sale Rate": 3830.0, "Stock": 30},
        {"ID": "MC-61", "Category": "Motor Cycle", "Name": "90/90-17 REAR TITAN (6PR)", "Cost Rate": 4457.63, "Sale Rate": 5260.0, "Stock": 20}
    ]
    st.session_state.inventory = pd.DataFrame(initial_data)

if "sales_history" not in st.session_state:
    st.session_state.sales_history = []

if "cart" not in st.session_state:
    st.session_state.cart = []

# ---------------------------------------------------------
# Login Screen
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.title("🔐 System Login")
    st.markdown("Please select your role and enter your name or admin password.")
    
    login_role = st.selectbox("Select Role:", ["Salesman", "Administrator (Admin)"])
    
    if login_role == "Salesman":
        sm_name_input = st.text_input("Enter Salesman Name:")
        if st.button("Login as Salesman"):
            if sm_name_input.strip() != "":
                st.session_state.logged_in = True
                st.session_state.user_role = "Salesman"
                st.session_state.current_salesman = sm_name_input
                st.rerun()
            else:
                st.warning("Please enter your name!")
    else:
        admin_pass = st.text_input("Enter Admin Password:", type="password")
        # Admin password is set to 'admin123'
        if st.button("Login as Admin"):
            if admin_pass == "admin123":
                st.session_state.logged_in = True
                st.session_state.user_role = "Admin"
                st.session_state.current_salesman = "Admin"
                st.rerun()
            else:
                st.error("Incorrect Password! Please enter the correct admin password.")
                
# ---------------------------------------------------------
# Main Application (After Login)
# ---------------------------------------------------------
else:
    col_top1, col_top2 = st.columns([6, 1])
    with col_top1:
        st.title(f"📦 Inventory & Billing System ({'Salesman Portal' if st.session_state.user_role == 'Salesman' else 'Admin Portal'})")
    with col_top2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = ""
            st.rerun()

    # 1. Salesman Portal
    if st.session_state.user_role == "Salesman":
        tab_sales, tab_print, tab_stock_view = st.tabs(["🛒 New Sale & Billing", "🖨️ Print Invoice", "📊 View Stock"])
        
        with tab_sales:
            st.header("New Sale Entry & Billing")
            st.info(f"Current Salesman: **{st.session_state.current_salesman}**")
            
            with st.expander("👤 Invoice Details (Shop & Area)", expanded=True):
                col_m2, col_m3 = st.columns(2)
                with col_m2:
                    shop_name = st.text_input("Shop Name:", "Enter Shop Name")
                with col_m3:
                    area_name = st.text_input("Area / Location:", "Enter Area Name")

            col1, col2 = st.columns([2, 1])
            
            with col1:
                category = st.selectbox("Select Category:", st.session_state.inventory["Category"].unique())
                filtered_items = st.session_state.inventory[st.session_state.inventory["Category"] == category]
                
                selected_item_name = st.selectbox("Select Product:", filtered_items["Name"].tolist())
                item_row = st.session_state.inventory[st.session_state.inventory["Name"] == selected_item_name].iloc[0]
                
                st.info(f"Available Stock: **{item_row['Stock']}** | Sale Rate: **Rs. {item_row['Sale Rate']:,.2f}**")
                
                qty = st.number_input("Quantity:", min_value=1, max_value=int(item_row["Stock"]) if item_row["Stock"] > 0 else 1, value=1)
                
                if st.button("Add Item to Cart"):
                    if item_row["Stock"] < qty:
                        st.error("Insufficient stock available!")
                    else:
                        st.session_state.cart.append({
                            "ID": item_row["ID"],
                            "Name": item_row["Name"],
                            "Qty": qty,
                            "Sale Rate": item_row["Sale Rate"],
                            "Total Amount": qty * item_row["Sale Rate"],
                            "Cost Rate": item_row["Cost Rate"]
                        })
                        st.success("Item added to cart successfully!")

            with col2:
                st.subheader("🛒 Current Cart")
                if len(st.session_state.cart) > 0:
                    cart_df = pd.DataFrame(st.session_state.cart)
                    cart_display = cart_df[["Name", "Qty", "Sale Rate", "Total Amount"]].copy()
                    cart_display.columns = ["Product Name", "Quantity", "Rate", "Total Amount"]
                    st.dataframe(cart_display, width='stretch')
                    
                    grand_total = cart_df["Total Amount"].sum()
                    st.markdown(f"### Grand Total: **Rs. {grand_total:,.2f}**")
                    
                    if st.button("Complete Sale & Save Invoice"):
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        invoice_items = st.session_state.cart.copy()
                        
                        for item in st.session_state.cart:
                            idx = st.session_state.inventory[st.session_state.inventory["ID"] == item["ID"]].index[0]
                            st.session_state.inventory.at[idx, "Stock"] -= item["Qty"]
                            
                            st.session_state.sales_history.append({
                                "Date": current_time,
                                "Salesman": st.session_state.current_salesman,
                                "Shop Name": shop_name,
                                "Area": area_name,
                                "Name": item["Name"],
                                "Qty": item["Qty"],
                                "Sale Rate": item["Sale Rate"],
                                "Total Sale": item["Total Amount"],
                                "Total Cost": item["Qty"] * item["Cost Rate"],
                                "Profit Amount": item["Total Amount"] - (item["Qty"] * item["Cost Rate"])
                            })
                        
                        st.session_state.invoices_history.append({
                            "Date": current_time,
                            "Salesman": st.session_state.current_salesman,
                            "Shop Name": shop_name,
                            "Area": area_name,
                            "Items": invoice_items,
                            "Total": grand_total
                        })
                        
                        st.success("Sale completed and saved! You can view/print it in the 'Print Invoice' tab.")
                        st.session_state.cart = []
                else:
                    st.info("Your cart is currently empty.")

        # Print Tab
        with tab_print:
            st.header("🖨️ Customer Invoices & Printing Section")
            if len(st.session_state.invoices_history) > 0:
                inv_options = [f"Date: {inv['Date']} | Shop: {inv['Shop Name']} | Total: Rs. {inv['Total']:,.2f}" for inv in st.session_state.invoices_history]
                selected_inv_str = st.selectbox("Select Invoice to Print:", inv_options)
                selected_idx = inv_options.index(selected_inv_str)
                selected_inv = st.session_state.invoices_history[selected_idx]
                
                st.markdown("---")
                bill_html = f"""
                <div style="border: 2px solid #333; padding: 20px; border-radius: 8px; background-color: #ffffff; color: #000; font-family: Arial, sans-serif;">
                    <h2 style="text-align: center; margin-bottom: 5px;">DIAMOND TYRES AGENCY</h2>
                    <p style="text-align: center; font-size: 14px; color: #555; margin-top: 0;">Quality & Durable Tyres Distributor</p>
                    <hr>
                    <p><b>Date & Time:</b> {selected_inv['Date']}<br>
                       <b>Salesman:</b> {selected_inv['Salesman']} | <b>Area:</b> {selected_inv['Area']}<br>
                       <b>Shop Name:</b> {selected_inv['Shop Name']}</p>
                    <hr>
                    <table style="width: 100%; border-collapse: collapse; text-align: left; margin-top: 10px;">
                        <thead>
                            <tr style="border-bottom: 2px solid #333; background-color: #f2f2f2;">
                                <th style="padding: 8px;">Product Name</th>
                                <th style="padding: 8px;">Qty</th>
                                <th style="padding: 8px;">Unit Price</th>
                                <th style="padding: 8px;">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                """
                for item in selected_inv['Items']:
                    bill_html += f"""
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 8px;">{item['Name']}</td>
                                <td style="padding: 8px;">{item['Qty']}</td>
                                <td style="padding: 8px;">Rs. {item['Sale Rate']:,.2f}</td>
                                <td style="padding: 8px;">Rs. {item['Total Amount']:,.2f}</td>
                            </tr>
                    """
                bill_html += f"""
                        </tbody>
                    </table>
                    <hr>
                    <h3 style="text-align: right; margin-top: 15px;">Grand Total: Rs. {selected_inv['Total']:,.2f}</h3>
                    <p style="text-align: center; font-size: 13px; color: #555; margin-top: 20px;">Thank you for your business!</p>
                </div>
                """
                st.components.v1.html(bill_html, height=450, scrolling=True)
                st.info("💡 You can print this invoice using your browser's print option (Ctrl + P).")
            else:
                st.info("No invoices generated yet.")

        with tab_stock_view:
            st.header("Available Products and Sale Rates")
            safe_inv = st.session_state.inventory[["ID", "Category", "Name", "Sale Rate", "Stock"]].copy()
            safe_inv.columns = ["ID", "Category", "Product Name", "Sale Rate", "Available Stock"]
            st.dataframe(safe_inv, width='stretch')

    # 2. Admin Portal
    elif st.session_state.user_role == "Admin":
        tab_sales_admin, tab_print_admin, tab_inventory, tab_cost_rates, tab_sale_rates, tab_reports = st.tabs([
            "🛒 Admin Sale Entry", 
            "🖨️ Print Invoices",
            "📊 Full Stock Dashboard (Cost & Margin)", 
            "⚙️ Change Cost Rate", 
            "🏷️ Change Sale Rate",
            "📈 Sales & Profit Reports"
        ])
        
        with tab_sales_admin:
            st.header("Admin Sale Entry")
            salesman_name = st.text_input("Salesman Name:", "Admin / Manager")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                shop_name = st.text_input("Shop Name:", "Enter Shop Name")
            with col_m2:
                area_name = st.text_input("Area / Location:", "Enter Area Name")
                
            category = st.selectbox("Select Category:", st.session_state.inventory["Category"].unique())
            filtered_items = st.session_state.inventory[st.session_state.inventory["Category"] == category]
            selected_item_name = st.selectbox("Select Product:", filtered_items["Name"].tolist())
            item_row = st.session_state.inventory[st.session_state.inventory["Name"] == selected_item_name].iloc[0]
            
            st.info(f"Stock: {item_row['Stock']} | Cost Rate: Rs. {item_row['Cost Rate']:,.2f} | Sale Rate: Rs. {item_row['Sale Rate']:,.2f}")
            qty = st.number_input("Quantity:", min_value=1, max_value=int(item_row["Stock"]) if item_row["Stock"] > 0 else 1, value=1)
            
            if st.button("Add to Admin Cart"):
                st.session_state.cart.append({
                    "ID": item_row["ID"], "Name": item_row["Name"], "Qty": qty,
                    "Cost Rate": item_row["Cost Rate"], "Sale Rate": item_row["Sale Rate"],
                    "Total Amount": qty * item_row["Sale Rate"]
                })
                st.success("Item added successfully!")
                
            if len(st.session_state.cart) > 0:
                cart_df = pd.DataFrame(st.session_state.cart)
                cart_disp = cart_df[["Name", "Qty", "Sale Rate", "Total Amount"]].copy()
                cart_disp.columns = ["Product Name", "Quantity", "Rate", "Total Amount"]
                st.dataframe(cart_disp, width='stretch')
                if st.button("Complete Admin Sale"):
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    invoice_items = st.session_state.cart.copy()
                    
                    for item in st.session_state.cart:
                        idx = st.session_state.inventory[st.session_state.inventory["ID"] == item["ID"]].index[0]
                        st.session_state.inventory.at[idx, "Stock"] -= item["Qty"]
                        st.session_state.sales_history.append({
                            "Date": current_time,
                            "Salesman": salesman_name, "Shop Name": shop_name, "Area": area_name,
                            "Name": item["Name"], "Qty": item["Qty"], "Cost Rate": item["Cost Rate"],
                            "Sale Rate": item["Sale Rate"], "Total Sale": item["Total Amount"],
                            "Total Cost": item["Qty"] * item["Cost Rate"],
                            "Profit Amount": item["Total Amount"] - (item["Qty"] * item["Cost Rate"])
                        })
                    
                    st.session_state.invoices_history.append({
                        "Date": current_time,
                        "Salesman": salesman_name,
                        "Shop Name": shop_name,
                        "Area": area_name,
                        "Items": invoice_items,
                        "Total": cart_df["Total Amount"].sum()
                    })
                    
                    st.success("Sale record and invoice saved successfully!")
                    st.session_state.cart = []

        with tab_print_admin:
            st.header("🖨️ Admin Invoice Printing Section")
            if len(st.session_state.invoices_history) > 0:
                inv_options = [f"Date: {inv['Date']} | Shop: {inv['Shop Name']} | Total: Rs. {inv['Total']:,.2f}" for inv in st.session_state.invoices_history]
                selected_inv_str = st.selectbox("Select Invoice to Print (Admin):", inv_options)
                selected_idx = inv_options.index(selected_inv_str)
                selected_inv = st.session_state.invoices_history[selected_idx]
                
                bill_html = f"""
                <div style="border: 2px solid #333; padding: 20px; border-radius: 8px; background-color: #ffffff; color: #000; font-family: Arial, sans-serif;">
                    <h2 style="text-align: center; margin-bottom: 5px;">DIAMOND TYRES AGENCY</h2>
                    <p style="text-align: center; font-size: 14px; color: #555; margin-top: 0;">Quality & Durable Tyres Distributor</p>
                    <hr>
                    <p><b>Date & Time:</b> {selected_inv['Date']}<br>
                       <b>Salesman:</b> {selected_inv['Salesman']} | <b>Area:</b> {selected_inv['Area']}<br>
                       <b>Shop Name:</b> {selected_inv['Shop Name']}</p>
                    <hr>
                    <table style="width: 100%; border-collapse: collapse; text-align: left; margin-top: 10px;">
                        <thead>
                            <tr style="border-bottom: 2px solid #333; background-color: #f2f2f2;">
                                <th style="padding: 8px;">Product Name</th>
                                <th style="padding: 8px;">Qty</th>
                                <th style="padding: 8px;">Unit Price</th>
                                <th style="padding: 8px;">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                """
                for item in selected_inv['Items']:
                    bill_html += f"""
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 8px;">{item['Name']}</td>
                                <td style="padding: 8px;">{item['Qty']}</td>
                                <td style="padding: 8px;">Rs. {item['Sale Rate']:,.2f}</td>
                                <td style="padding: 8px;">Rs. {item['Total Amount']:,.2f}</td>
                            </tr>
                    """
                bill_html += f"""
                        </tbody>
                    </table>
                    <hr>
                    <h3 style="text-align: right; margin-top: 15px;">Grand Total: Rs. {selected_inv['Total']:,.2f}</h3>
                    <p style="text-align: center; font-size: 13px; color: #555; margin-top: 20px;">Thank you for your business!</p>
                </div>
                """
                st.components.v1.html(bill_html, height=450, scrolling=True)
            else:
                st.info("No invoices found.")

        with tab_inventory:
            st.header("Current Inventory (Confidential - Admin Only)")
            df_inv = st.session_state.inventory.copy()
            df_inv["Margin (Rs)"] = df_inv["Sale Rate"] - df_inv["Cost Rate"]
            df_inv["Margin (%)"] = ((df_inv["Margin (Rs)"] / df_inv["Cost Rate"]) * 100).round(2)
            df_inv.columns = ["ID", "Category", "Product Name", "Cost Rate", "Sale Rate", "Available Stock", "Margin (Rs)", "Margin (%)"]
            st.dataframe(df_inv, width='stretch')

        with tab_cost_rates:
            st.header("⚙️ Change Cost Rate (Admin Only)")
            selected_id_c = st.selectbox("Select Product (Cost):", st.session_state.inventory["ID"] + " - " + st.session_state.inventory["Name"])
            item_id_c = selected_id_c.split(" - ")[0]
            curr_c = st.session_state.inventory[st.session_state.inventory["ID"] == item_id_c].iloc[0]["Cost Rate"]
            new_cost = st.number_input("Enter New Cost Rate:", min_value=0.0, value=float(curr_c), step=10.0)
            if st.button("Update Cost Rate"):
                idx = st.session_state.inventory[st.session_state.inventory["ID"] == item_id_c].index[0]
                st.session_state.inventory.at[idx, "Cost Rate"] = new_cost
                st.success("Cost rate updated successfully!")

        with tab_sale_rates:
            st.header("🏷️ Change Sale Rate (Admin Only)")
            selected_id_s = st.selectbox("Select Product (Sale):", st.session_state.inventory["ID"] + " - " + st.session_state.inventory["Name"])
            item_id_s = selected_id_s.split(" - ")[0]
            curr_row_s = st.session_state.inventory[st.session_state.inventory["ID"] == item_id_s].iloc[0]
            new_sale = st.number_input("Enter New Sale Rate:", min_value=0.0, value=float(curr_row_s["Sale Rate"]), step=10.0)
            if st.button("Update Sale Rate"):
                idx = st.session_state.inventory[st.session_state.inventory["ID"] == item_id_s].index[0]
                st.session_state.inventory.at[idx, "Sale Rate"] = new_sale
                st.success("Sale rate updated successfully!")

        with tab_reports:
            st.header("📈 Profit and Sales Reports (Admin Only)")
            if len(st.session_state.sales_history) > 0:
                sales_df = pd.DataFrame(st.session_state.sales_history)
                total_revenue = sales_df["Total Sale"].sum()
                total_profit = sales_df["Profit Amount"].sum()
                
                col_r1, col_r2 = st.columns(2)
                col_r1.metric("Total Sales", f"Rs. {total_revenue:,.2f}")
                col_r2.metric("Total Net Profit", f"Rs. {total_profit:,.2f}")
                
                sales_disp = sales_df.copy()
                sales_disp.columns = ["Date", "Salesman", "Shop Name", "Area", "Product Name", "Qty", "Sale Rate", "Total Sale", "Total Cost", "Profit (Rs)"]
                st.dataframe(sales_disp, width='stretch')
            else:
                st.info("No sales records available yet.")