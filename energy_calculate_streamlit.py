import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide"
)

# Title and header
st.title("⚡ Energy Consumption Calculator")
st.markdown("Calculate your daily energy consumption based on your home setup")

# Create two columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Personal Information")
    
    # Personal details
    name = st.text_input("Enter your name:", placeholder="John Doe")
    age = st.number_input("Enter your age:", min_value=1, max_value=120, value=25)
    area = st.text_input("Enter your area:", placeholder="Downtown")
    city = st.text_input("Enter your city:", placeholder="Mumbai")
    
    st.header("House Details")
    
    # House type
    home_type = st.selectbox(
        "Choose type of House:",
        ["Flat", "Tenament"]
    )
    
    # Room type
    rooms = st.selectbox(
        "Choose room type:",
        ["1BHK", "2BHK", "3BHK"]
    ).lower()

with col2:
    st.header("Day Selection")
    
    # Day selection
    selected_day = st.selectbox(
        "Select day for energy calculation:",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    
    st.header("Appliances")
    
    # Appliances
    has_ac = st.radio("Do you have AC?", ["Yes", "No"])
    num_ac = 0
    if has_ac == "Yes":
        num_ac = st.number_input("How many ACs do you have?", min_value=1, max_value=10, value=1)
    
    has_fridge = st.radio("Do you have Fridge?", ["Yes", "No"])
    has_washing = st.radio("Do you have washing machine?", ["Yes", "No"])

# Calculate button
if st.button("Calculate Energy Consumption", type="primary"):
    if name and age and area and city and selected_day:
        # Initialize energy calculation
        cal_energy = 0
        
        # Set fans and lights based on room type
        if rooms == "1bhk":
            fans = 2
            lights = 2
        elif rooms == "2bhk":
            fans = 3
            lights = 3
        elif rooms == "3bhk":
            fans = 3
            lights = 3
        else:
            st.error("Invalid room type selected")
            st.stop()
        
        # Day-based energy consumption multipliers
        day_multipliers = {
            "Monday": 1.0,      # Regular working day
            "Tuesday": 1.0,     # Regular working day
            "Wednesday": 1.0,   # Regular working day
            "Thursday": 1.0,    # Regular working day
            "Friday": 1.1,      # Slightly higher usage
            "Saturday": 1.3,    # Weekend - higher usage
            "Sunday": 1.2       # Weekend - moderate usage
        }
        
        # Get multiplier for selected day
        day_multiplier = day_multipliers.get(selected_day, 1.0)
        
        # Calculate base energy (fans + lights)
        base_energy = (fans * 0.4) + (lights * 0.8)
        
        # Add AC consumption
        ac_energy = 0
        if has_ac == "Yes":
            ac_energy = num_ac * 3
        
        # Add fridge consumption (constant regardless of day)
        fridge_energy = 0
        if has_fridge == "Yes":
            fridge_energy = 4
        
        # Add washing machine consumption
        washing_energy = 0
        if has_washing == "Yes":
            washing_energy = 2
        
        # Calculate total energy with day multiplier
        # Note: Fridge consumption remains constant, other appliances vary by day
        cal_energy = ((base_energy + ac_energy + washing_energy) * day_multiplier) + fridge_energy
        
        # Display results
        st.success("✅ Calculation Complete!")
        
        # Create results section
        st.header("📊 Energy Consumption Results")
        
        # Display user info
        st.subheader("User Information")
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.write(f"**Name:** {name}")
            st.write(f"**Age:** {age}")
        with info_col2:
            st.write(f"**Area:** {area}")
            st.write(f"**City:** {city}")
        
        st.write(f"**House Type:** {home_type}")
        st.write(f"**Room Configuration:** {rooms.upper()}")
        st.write(f"**Selected Day:** {selected_day}")
        st.write(f"**Day Usage Factor:** {day_multiplier}x")
        
        # Display appliance breakdown
        st.subheader("Appliance Breakdown")
        
        breakdown_data = {
            "Appliance": ["Fans", "Lights"],
            "Quantity": [fans, lights],
            "Base Power (kW)": [0.4, 0.8],
            "Base Consumption (kWh)": [fans * 0.4, lights * 0.8],
            "Day-Adjusted Consumption (kWh)": [fans * 0.4 * day_multiplier, lights * 0.8 * day_multiplier]
        }
        
        if has_ac == "Yes":
            breakdown_data["Appliance"].append("Air Conditioner")
            breakdown_data["Quantity"].append(num_ac)
            breakdown_data["Base Power (kW)"].append(3.0)
            breakdown_data["Base Consumption (kWh)"].append(num_ac * 3)
            breakdown_data["Day-Adjusted Consumption (kWh)"].append(num_ac * 3 * day_multiplier)
        
        if has_fridge == "Yes":
            breakdown_data["Appliance"].append("Refrigerator")
            breakdown_data["Quantity"].append(1)
            breakdown_data["Base Power (kW)"].append(4.0)
            breakdown_data["Base Consumption (kWh)"].append(4)
            breakdown_data["Day-Adjusted Consumption (kWh)"].append(4)  # Constant consumption
        
        if has_washing == "Yes":
            breakdown_data["Appliance"].append("Washing Machine")
            breakdown_data["Quantity"].append(1)
            breakdown_data["Base Power (kW)"].append(2.0)
            breakdown_data["Base Consumption (kWh)"].append(2)
            breakdown_data["Day-Adjusted Consumption (kWh)"].append(2 * day_multiplier)
        
        # Create and display table
        df = pd.DataFrame(breakdown_data)
        st.dataframe(df, use_container_width=True)
        
        # Display total consumption
        st.subheader("Total Energy Consumption")
        
        # Create metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"{selected_day} Consumption", f"{cal_energy:.1f} kWh")
        with col2:
            st.metric("Weekly Avg Consumption", f"{cal_energy * 7 / day_multiplier:.1f} kWh")
        with col3:
            st.metric("Monthly Avg Consumption", f"{cal_energy * 30 / day_multiplier:.1f} kWh")
        
        # Weekly breakdown with day-specific calculations
        st.subheader("Weekly Energy Consumption Breakdown")
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        weekly_consumption = []
        for day in days:
            day_mult = day_multipliers.get(day, 1.0)
            day_energy = ((base_energy + ac_energy + washing_energy) * day_mult) + fridge_energy
            weekly_consumption.append(day_energy)
        
        weekly_data = {
            "Day": days,
            "Usage Factor": [day_multipliers.get(day, 1.0) for day in days],
            "Energy Consumption (kWh)": weekly_consumption
        }
        
        weekly_df = pd.DataFrame(weekly_data)
        st.dataframe(weekly_df, use_container_width=True)
        
        # Create a bar chart showing variation across days
        st.subheader("Daily Energy Consumption Chart")
        chart_data = weekly_df.set_index("Day")["Energy Consumption (kWh)"]
        st.bar_chart(chart_data)
        
        # Highlight current day
        if selected_day in days:
            current_day_consumption = weekly_consumption[days.index(selected_day)]
            st.info(f"📅 **{selected_day}** energy consumption: **{current_day_consumption:.1f} kWh**")
        
        # Energy saving tips based on day
        st.subheader("💡 Day-Specific Energy Saving Tips")
        
        if selected_day in ["Saturday", "Sunday"]:
            weekend_tips = [
                "Weekend usage is typically higher due to more time spent at home",
                "Consider using natural light during daytime to reduce lighting costs",
                "Plan energy-intensive activities (washing, ironing) during off-peak hours",
                "Use timers for appliances to avoid unnecessary usage"
            ]
            for tip in weekend_tips:
                st.write(f"• {tip}")
        else:
            weekday_tips = [
                "Weekday usage is generally lower due to work/school schedules",
                "Turn off lights and fans when leaving for work",
                "Use programmable thermostats to optimize AC usage",
                "Consider running washing machine/dishwasher during off-peak hours"
            ]
            for tip in weekday_tips:
                st.write(f"• {tip}")
        
        # General tips
        st.write("**General Tips:**")
        general_tips = [
            "Use LED bulbs instead of incandescent bulbs to save up to 80% energy",
            "Set your AC temperature to 24°C or higher for optimal efficiency",
            "Unplug appliances when not in use to avoid phantom power consumption",
            "Regular maintenance of appliances improves their efficiency"
        ]
        
        for tip in general_tips:
            st.write(f"• {tip}")
        
    else:
        st.error("Please fill in all the required fields including day selection before calculating.")

# Footer
st.markdown("---")
st.markdown("*This calculator provides estimates based on typical appliance power consumption. Actual consumption may vary based on usage patterns and appliance efficiency.*")
