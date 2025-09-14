import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime
import time

# Database connection function
def get_connection():
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            user="cricapp",
            password="Strong!Pass#123",
            database="Cricbuzz_project",
            port=3306,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

# CRUD operations class
class CricketCRUD:
    def __init__(self):
        self.conn = get_connection()
    
    def execute_query(self, query, params=None, fetch=True):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    result = cursor.fetchall()
                    self.conn.commit()
                    return result
                else:
                    self.conn.commit()
                    return cursor.rowcount
        except Exception as e:
            st.error(f"Query execution failed: {e}")
            return None
    
    def get_table_data(self, table_name, where_clause=""):
        query = f"SELECT * FROM `{table_name}` {where_clause} LIMIT 1000"
        return self.execute_query(query)
    
    def get_highest_scores_by_format(self, format_type):
        query = "SELECT * FROM `highest_scores` WHERE Format = %s"
        return self.execute_query(query, (format_type,))
    
    def get_player_by_id(self, player_id):
        query = "SELECT * FROM `players_with_stats` WHERE playerId = %s"
        return self.execute_query(query, (player_id,))
    
    def insert_data(self, table_name, data):
        columns = ', '.join([f"`{key}`" for key in data.keys()])
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
        return self.execute_query(query, tuple(data.values()), fetch=False)
    
    def update_data(self, table_name, primary_key, pk_value, data):
        set_clause = ', '.join([f"`{key}` = %s" for key in data.keys()])
        query = f"UPDATE `{table_name}` SET {set_clause} WHERE `{primary_key}` = %s"
        params = tuple(data.values()) + (pk_value,)
        return self.execute_query(query, params, fetch=False)
    
    def delete_data(self, table_name, primary_key, pk_value):
        query = f"DELETE FROM `{table_name}` WHERE `{primary_key}` = %s"
        return self.execute_query(query, (pk_value,), fetch=False)
    
    def get_all_player_ids(self):
        query = "SELECT playerId, playerName FROM `players_with_stats` ORDER BY playerId LIMIT 1000"
        return self.execute_query(query)
    
    def close(self):
        if self.conn:
            self.conn.close()

# Helper function to get primary key column
def get_primary_key_column(df):
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['id', 'pk', 'primary']):
            return col
    return df.columns[0] if not df.empty else None

# Main application
def main():
    st.set_page_config(page_title="Cricket Database CRUD", layout="wide")
    st.title("🏏 Cricket Database Management System")
    
    # Initialize CRUD instance
    crud = CricketCRUD()
    if not crud.conn:
        st.error("Cannot connect to database. Please check your connection settings.")
        return


    try:
        # Sidebar for table selection
        tables = [
            "cricket_series_2024", "highest_scores", "indian_players", 
            "international_teams", "match_results", "players_with_stats",
            "recent_matches", "teams_players", "top_odi_runs", 
            "top_test_runs", "venues",
            "matches", "test_teams", "recent_innings", "recent_batting_scorecard",
            "partnerships",
            # New cricket performance tables
            "batting_2", "bowling_2", "indian_matches"
        ]


        
        selected_table = st.sidebar.selectbox("Select Table", tables)
        operation = st.sidebar.radio("Operation", ["View", "Create", "Update", "Delete"])

        
        st.header(f"{operation} - {selected_table}")
        
        # Special handling for highest_scores table
        if selected_table == "highest_scores" and operation == "View":
            st.subheader("Search by Format")
            format_type = st.selectbox("Select Format", ["Test", "ODI", "T20"], index=0)
            
            if st.button("Search by Format"):
                data = crud.get_highest_scores_by_format(format_type)
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                    st.metric(f"Total {format_type} Records", len(df))
                else:
                    st.warning(f"No records found for {format_type} format")
            
            # Also show all data option
            if st.checkbox("Show all highest scores"):
                data = crud.get_table_data(selected_table)
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                    st.metric("Total Records", len(df))
        
        # Special handling for players_with_stats in Update operation
        elif selected_table == "players_with_stats" and operation == "Update":
            st.subheader("Search Player by ID")
            
            # First, get all player IDs for selection
            all_players = crud.get_all_player_ids()
            if all_players:
                # Create a mapping of playerId to playerName for display
                player_options = {f"{player['playerId']} - {player['playerName']}": player['playerId'] for player in all_players}
                selected_display = st.selectbox("Select Player", list(player_options.keys()))
                selected_player_id = player_options[selected_display]
                
                if st.button("Load Player Data"):
                    player_data = crud.get_player_by_id(selected_player_id)
                    if player_data:
                        df = pd.DataFrame(player_data)
                        st.success(f"Loaded data for Player ID: {selected_player_id}")
                        
                        # Display current player info
                        player = player_data[0]
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Player Name", player['playerName'])
                        col2.metric("Team", player['teamName'])
                        col3.metric("Country", player['countryName'])
                        
                        st.subheader("Update Player Statistics")
                        
                        # Group fields by category for better organization
                        batting_stats = {}
                        bowling_stats = {}
                        personal_info = {}
                        
                        for col in df.columns:
                            if any(keyword in col.lower() for keyword in ['bat', 'runs', 'average', 'sr', '50s', '100s', 'innings', 'matches']):
                                batting_stats[col] = player[col]
                            elif any(keyword in col.lower() for keyword in ['bowl', 'wickets', 'eco', 'maiden', 'overs']):
                                bowling_stats[col] = player[col]
                            else:
                                personal_info[col] = player[col]
                        
                        update_fields = {}
                        
                        # Personal Info
                        with st.expander("Personal Information"):
                            for col, value in personal_info.items():
                                if col != 'playerId':
                                    if pd.api.types.is_numeric_dtype(df[col]) and 'id' not in col.lower():
                                        update_fields[col] = st.number_input(
                                            col, value=float(value) if value is not None else 0.0,
                                            key=f"personal_{col}"
                                        )
                                    else:
                                        update_fields[col] = st.text_input(
                                            col, value=str(value) if value is not None else "",
                                            key=f"personal_{col}"
                                        )
                        
                        # Batting Stats
                        with st.expander("Batting Statistics"):
                            for col, value in batting_stats.items():
                                if pd.api.types.is_numeric_dtype(df[col]):
                                    update_fields[col] = st.number_input(
                                        col, value=float(value) if value is not None else 0.0,
                                        key=f"batting_{col}"
                                    )
                                else:
                                    update_fields[col] = st.text_input(
                                        col, value=str(value) if value is not None else "",
                                        key=f"batting_{col}"
                                    )
                        
                        # Bowling Stats
                        with st.expander("Bowling Statistics"):
                            for col, value in bowling_stats.items():
                                if pd.api.types.is_numeric_dtype(df[col]):
                                    update_fields[col] = st.number_input(
                                        col, value=float(value) if value is not None else 0.0,
                                        key=f"bowling_{col}"
                                    )
                                else:
                                    update_fields[col] = st.text_input(
                                        col, value=str(value) if value is not None else "",
                                        key=f"bowling_{col}"
                                    )
                        
                        if st.button("Update Player Record"):
                            # Remove None values from update_fields
                            update_fields = {k: v for k, v in update_fields.items() if v is not None}
                            if update_fields:
                                result = crud.update_data(selected_table, 'playerId', selected_player_id, update_fields)
                                if result:
                                    st.success("Player record updated successfully!")
                                    time.sleep(2)
                                    st.rerun()
                            else:
                                st.warning("No fields to update")
                    else:
                        st.error("Player not found!")
            else:
                st.warning("No players found in the database")
        
        # Default behavior for other tables
        else:
            # Get table data
            data = crud.get_table_data(selected_table)
            if data is None:
                st.error("Failed to fetch data")
                return
            
            if not data:
                st.warning("No data found in the table")
                return
                
            df = pd.DataFrame(data)
            
            if operation == "View":
                st.dataframe(df, use_container_width=True)
                
                # Show statistics
                st.subheader("Table Information")
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Records", len(df))
                col2.metric("Columns", len(df.columns))
                col3.metric("Preview", f"{len(df)} rows")
                
            elif operation == "Create":
                st.subheader("Add New Record")
                
                # Get column information
                exclude_cols = ['created_at', 'updated_at']
                input_fields = {}
                
                for col in df.columns:
                    if not any(exclude in col.lower() for exclude in exclude_cols):
                        col_type = str(df[col].dtype)
                        
                        if 'int' in col_type:
                            input_fields[col] = st.number_input(col, value=0, key=f"create_{col}")
                        elif 'float' in col_type or 'decimal' in col_type:
                            input_fields[col] = st.number_input(col, value=0.0, key=f"create_{col}")
                        elif 'date' in col_type:
                            input_fields[col] = st.date_input(col, key=f"create_{col}")
                        elif 'datetime' in col_type:
                            input_fields[col] = st.datetime_input(col, key=f"create_{col}")
                        else:
                            input_fields[col] = st.text_input(col, key=f"create_{col}")
                
                if st.button("Add Record"):
                    if all(value is not None for value in input_fields.values()):
                        result = crud.insert_data(selected_table, input_fields)
                        if result:
                            st.success("Record added successfully!")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.error("Please fill all fields")
            
            elif operation == "Update" and selected_table != "players_with_stats":
                st.subheader("Update Record")
                
                if not df.empty:
                    primary_key_col = get_primary_key_column(df)
                    
                    if primary_key_col:
                        record_id = st.selectbox(f"Select {primary_key_col}", df[primary_key_col].tolist())
                        selected_record = df[df[primary_key_col] == record_id].iloc[0]
                        
                        st.write("Current values:")
                        st.json(selected_record.to_dict())
                        
                        # Input fields for update
                        update_fields = {}
                        for col in df.columns:
                            if col != primary_key_col and not any(exclude in col.lower() for exclude in ['created_at', 'updated_at']):
                                current_val = selected_record[col]
                                
                                if pd.api.types.is_numeric_dtype(df[col]):
                                    update_fields[col] = st.number_input(
                                        col, 
                                        value=float(current_val) if pd.notnull(current_val) else 0.0,
                                        key=f"update_{col}"
                                    )
                                elif pd.api.types.is_datetime64_any_dtype(df[col]):
                                    update_fields[col] = st.date_input(
                                        col, 
                                        value=current_val if pd.notnull(current_val) else datetime.now().date(),
                                        key=f"update_{col}"
                                    )
                                else:
                                    update_fields[col] = st.text_input(
                                        col, 
                                        value=str(current_val) if pd.notnull(current_val) else "",
                                        key=f"update_{col}"
                                    )
                        
                        if st.button("Update Record"):
                            result = crud.update_data(selected_table, primary_key_col, record_id, update_fields)
                            if result:
                                st.success("Record updated successfully!")
                                time.sleep(1)
                                st.rerun()
                    else:
                        st.error("Could not identify primary key column")
                else:
                    st.warning("No records to update")
            
            elif operation == "Delete":
                st.subheader("Delete Record")
                
                if not df.empty:
                    primary_key_col = get_primary_key_column(df)
                    
                    if primary_key_col:
                        record_id = st.selectbox(f"Select {primary_key_col} to delete", df[primary_key_col].tolist())
                        selected_record = df[df[primary_key_col] == record_id].iloc[0]
                        
                        st.write("Record to be deleted:")
                        st.json(selected_record.to_dict())
                        
                        if st.button("Delete Record", type="secondary"):
                            confirm = st.checkbox("I confirm I want to delete this record")
                            if confirm:
                                result = crud.delete_data(selected_table, primary_key_col, record_id)
                                if result:
                                    st.success("Record deleted successfully!")
                                    time.sleep(1)
                                    st.rerun()
                    else:
                        st.error("Could not identify primary key column")
                else:
                    st.warning("No records to delete")
    
    finally:
        # Ensure connection is closed
        crud.close()

# Run the application
if __name__ == "__main__":
    main()