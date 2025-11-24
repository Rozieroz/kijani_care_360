import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional
import os

class CanopyVisualizer:
    def __init__(self):
        self.output_dir = "static/visualizations"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("viridis")
    
    def create_coverage_trend_chart(self, start_year: int = 2000, end_year: int = 2024, region: Optional[str] = None):
        """Create forest coverage trend chart"""
        
        # Sample data
        years = list(range(start_year, end_year + 1, 5))
        coverage = [6.2, 6.0, 6.9, 7.4, 8.8, 12.13][:len(years)]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create the plot
        ax.plot(years, coverage, marker='o', linewidth=3, markersize=8, color='#2E8B57')
        ax.fill_between(years, coverage, alpha=0.3, color='#2E8B57')
        
        # Add target line
        ax.axhline(y=10, color='red', linestyle='--', alpha=0.7, label='10% Target')
        
        # Styling
        ax.set_title(f'Kenya Forest Coverage Trend ({start_year}-{end_year})', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Forest Coverage (%)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Add annotations
        for i, (year, cov) in enumerate(zip(years, coverage)):
            ax.annotate(f'{cov}%', (year, cov), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontsize=10)
        
        plt.tight_layout()
        
        filename = f"coverage_trend_{start_year}_{end_year}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_regional_comparison_chart(self):
        """Create regional forest coverage comparison chart"""
        
        regions = ['Western', 'Central', 'Coast', 'Rift Valley', 'Eastern', 'Northern']
        coverage = [18.5, 15.2, 11.7, 8.9, 5.3, 2.1]
        colors = ['#228B22', '#32CD32', '#90EE90', '#FFD700', '#FFA500', '#FF6347']
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        bars = ax.barh(regions, coverage, color=colors)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, coverage)):
            ax.text(value + 0.3, bar.get_y() + bar.get_height()/2, 
                   f'{value}%', va='center', fontweight='bold')
        
        # Add national average line
        national_avg = 12.13
        ax.axvline(x=national_avg, color='red', linestyle='--', alpha=0.7, 
                  label=f'National Average ({national_avg}%)')
        
        ax.set_title('Forest Coverage by Region (2024)', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Forest Coverage (%)', fontsize=12)
        ax.set_ylabel('Region', fontsize=12)
        ax.legend()
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        filename = "regional_comparison.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_deforestation_hotspots_map(self):
        """Create deforestation hotspots visualization"""
        
        # Sample hotspot data
        hotspots = {
            'Mau Forest': {'lat': -0.5, 'lng': 35.8, 'loss': 107},
            'Mt. Kenya': {'lat': -0.15, 'lng': 37.3, 'loss': 45},
            'Aberdare': {'lat': -0.4, 'lng': 36.7, 'loss': 32},
            'Kakamega': {'lat': 0.3, 'lng': 34.9, 'loss': 28}
        }
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create scatter plot
        lats = [data['lat'] for data in hotspots.values()]
        lngs = [data['lng'] for data in hotspots.values()]
        losses = [data['loss'] for data in hotspots.values()]
        names = list(hotspots.keys())
        
        scatter = ax.scatter(lngs, lats, s=[loss*5 for loss in losses], 
                           c=losses, cmap='Reds', alpha=0.7, edgecolors='black')
        
        # Add labels
        for i, name in enumerate(names):
            ax.annotate(name, (lngs[i], lats[i]), xytext=(5, 5), 
                       textcoords='offset points', fontsize=10, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('Forest Loss (km²)', fontsize=12)
        
        ax.set_title('Deforestation Hotspots in Kenya (2000-2020)', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filename = "deforestation_hotspots.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_reforestation_progress_chart(self):
        """Create reforestation progress chart"""
        
        years = [2019, 2020, 2021, 2022, 2023, 2024]
        trees_planted = [1.8, 2.5, 3.2, 4.1, 5.8, 7.5]  # in millions
        survival_rates = [65, 68, 72, 75, 78, 80]  # percentage
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Trees planted chart
        bars1 = ax1.bar(years, trees_planted, color='#228B22', alpha=0.8)
        ax1.set_title('Trees Planted per Year', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Trees Planted (Millions)', fontsize=12)
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars1, trees_planted):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{value}M', ha='center', va='bottom', fontweight='bold')
        
        # Survival rates chart
        line = ax2.plot(years, survival_rates, marker='o', linewidth=3, 
                       markersize=8, color='#FF6347')
        ax2.fill_between(years, survival_rates, alpha=0.3, color='#FF6347')
        ax2.set_title('Tree Survival Rates', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Year', fontsize=12)
        ax2.set_ylabel('Survival Rate (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Add value labels
        for year, rate in zip(years, survival_rates):
            ax2.annotate(f'{rate}%', (year, rate), textcoords="offset points",
                        xytext=(0,10), ha='center', fontsize=10)
        
        plt.tight_layout()
        
        filename = "reforestation_progress.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath