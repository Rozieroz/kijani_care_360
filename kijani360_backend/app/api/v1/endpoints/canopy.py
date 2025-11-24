from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
import json
import os
from app.utils.visualization import CanopyVisualizer

router = APIRouter()

# Initialize visualizer
visualizer = CanopyVisualizer()

@router.get("/coverage-data")
def get_canopy_coverage_data(
    start_year: int = Query(2000),
    end_year: int = Query(2024),
    region: Optional[str] = Query(None)
):
    """Get canopy coverage data for visualization"""
    
    # Kenya canopy coverage data (approximate)
    coverage_data = [
        {"year": 2000, "coverage_percentage": 6.2, "area_km2": 36000, "region": "national"},
        {"year": 2005, "coverage_percentage": 6.0, "area_km2": 34800, "region": "national"},
        {"year": 2010, "coverage_percentage": 6.9, "area_km2": 40000, "region": "national"},
        {"year": 2015, "coverage_percentage": 7.4, "area_km2": 42900, "region": "national"},
        {"year": 2020, "coverage_percentage": 8.8, "area_km2": 51000, "region": "national"},
        {"year": 2024, "coverage_percentage": 12.13, "area_km2": 70400, "region": "national"}
    ]
    
    # Regional breakdown for 2024
    regional_data = {
        "central": {"coverage_percentage": 15.2, "area_km2": 8800},
        "western": {"coverage_percentage": 18.5, "area_km2": 12400},
        "rift_valley": {"coverage_percentage": 8.9, "area_km2": 15200},
        "eastern": {"coverage_percentage": 5.3, "area_km2": 8900},
        "coast": {"coverage_percentage": 11.7, "area_km2": 9800},
        "northern": {"coverage_percentage": 2.1, "area_km2": 3200}
    }
    
    # Filter by year range
    filtered_data = [
        d for d in coverage_data 
        if start_year <= d["year"] <= end_year
    ]
    
    result = {
        "national_data": filtered_data,
        "regional_data": regional_data,
        "metadata": {
            "data_source": "Kenya Forest Service & Global Forest Watch",
            "last_updated": "2024",
            "total_land_area_km2": 580367,
            "target_coverage_percentage": 10.0,
            "current_coverage_percentage": 12.13
        }
    }
    
    if region and region in regional_data:
        result["selected_region"] = {
            "name": region,
            **regional_data[region]
        }
    
    return result

@router.get("/deforestation-hotspots")
def get_deforestation_hotspots():
    """Get deforestation hotspot data"""
    return {
        "hotspots": [
            {
                "name": "Mau Forest Complex",
                "location": {"lat": -0.5, "lng": 35.8},
                "area_lost_km2": 107,
                "period": "2000-2020",
                "severity": "high",
                "causes": ["Agricultural expansion", "Illegal logging", "Settlement"]
            },
            {
                "name": "Mt. Kenya Forest",
                "location": {"lat": -0.15, "lng": 37.3},
                "area_lost_km2": 45,
                "period": "2000-2020",
                "severity": "medium",
                "causes": ["Agricultural encroachment", "Charcoal production"]
            },
            {
                "name": "Aberdare Forest",
                "location": {"lat": -0.4, "lng": 36.7},
                "area_lost_km2": 32,
                "period": "2000-2020",
                "severity": "medium",
                "causes": ["Tea farming expansion", "Settlement"]
            },
            {
                "name": "Kakamega Forest",
                "location": {"lat": 0.3, "lng": 34.9},
                "area_lost_km2": 28,
                "period": "2000-2020",
                "severity": "high",
                "causes": ["Agricultural pressure", "Fuel wood collection"]
            }
        ],
        "summary": {
            "total_area_lost_km2": 212,
            "period": "2000-2020",
            "primary_causes": [
                "Agricultural expansion (45%)",
                "Illegal logging (25%)",
                "Settlement (20%)",
                "Charcoal production (10%)"
            ]
        }
    }

@router.get("/reforestation-progress")
def get_reforestation_progress():
    """Get reforestation and afforestation progress data"""
    return {
        "progress": [
            {
                "year": 2019,
                "trees_planted": 1800000,
                "area_restored_hectares": 1200,
                "survival_rate": 0.65
            },
            {
                "year": 2020,
                "trees_planted": 2500000,
                "area_restored_hectares": 1800,
                "survival_rate": 0.68
            },
            {
                "year": 2021,
                "trees_planted": 3200000,
                "area_restored_hectares": 2400,
                "survival_rate": 0.72
            },
            {
                "year": 2022,
                "trees_planted": 4100000,
                "area_restored_hectares": 3100,
                "survival_rate": 0.75
            },
            {
                "year": 2023,
                "trees_planted": 5800000,
                "area_restored_hectares": 4200,
                "survival_rate": 0.78
            },
            {
                "year": 2024,
                "trees_planted": 7500000,
                "area_restored_hectares": 5500,
                "survival_rate": 0.80
            }
        ],
        "targets": {
            "trees_by_2030": 15000000000,  # 15 billion trees
            "forest_coverage_target": 10.0,
            "current_progress": 12.13
        },
        "key_initiatives": [
            "National Tree Growing Day",
            "School Greening Program",
            "Community Forest Associations",
            "Private Sector Partnerships"
        ]
    }

@router.get("/county-rankings")
def get_county_forest_rankings():
    """Get forest coverage rankings by county"""
    return {
        "rankings": [
            {"rank": 1, "county": "Elgeyo Marakwet", "coverage_percentage": 45.2},
            {"rank": 2, "county": "Nyandarua", "coverage_percentage": 32.8},
            {"rank": 3, "county": "Nyeri", "coverage_percentage": 28.5},
            {"rank": 4, "county": "Kiambu", "coverage_percentage": 25.1},
            {"rank": 5, "county": "Murang'a", "coverage_percentage": 22.7},
            {"rank": 6, "county": "Kakamega", "coverage_percentage": 21.3},
            {"rank": 7, "county": "Kericho", "coverage_percentage": 19.8},
            {"rank": 8, "county": "Bomet", "coverage_percentage": 18.4},
            {"rank": 9, "county": "Trans Nzoia", "coverage_percentage": 16.9},
            {"rank": 10, "county": "Uasin Gishu", "coverage_percentage": 15.2}
        ],
        "bottom_counties": [
            {"county": "Mandera", "coverage_percentage": 0.8},
            {"county": "Wajir", "coverage_percentage": 1.2},
            {"county": "Garissa", "coverage_percentage": 1.5},
            {"county": "Turkana", "coverage_percentage": 2.1},
            {"county": "Marsabit", "coverage_percentage": 2.8}
        ],
        "national_average": 12.13
    }

@router.get("/generate-visualization")
def generate_canopy_visualization(
    visualization_type: str = Query("coverage_trend"),
    start_year: int = Query(2000),
    end_year: int = Query(2024),
    region: Optional[str] = Query(None)
):
    """Generate canopy coverage visualization"""
    try:
        if visualization_type == "coverage_trend":
            chart_path = visualizer.create_coverage_trend_chart(start_year, end_year, region)
        elif visualization_type == "regional_comparison":
            chart_path = visualizer.create_regional_comparison_chart()
        elif visualization_type == "deforestation_map":
            chart_path = visualizer.create_deforestation_hotspots_map()
        else:
            raise HTTPException(status_code=400, detail="Invalid visualization type")
        
        if os.path.exists(chart_path):
            return FileResponse(
                chart_path,
                media_type="image/png",
                filename=f"canopy_{visualization_type}_{start_year}_{end_year}.png"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate visualization")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating visualization: {str(e)}")

@router.get("/satellite-data")
def get_satellite_data_info():
    """Get information about satellite data sources"""
    return {
        "data_sources": [
            {
                "name": "Landsat",
                "provider": "NASA/USGS",
                "resolution": "30m",
                "temporal_coverage": "1972-present",
                "update_frequency": "16 days"
            },
            {
                "name": "Sentinel-2",
                "provider": "ESA",
                "resolution": "10m",
                "temporal_coverage": "2015-present",
                "update_frequency": "5 days"
            },
            {
                "name": "MODIS",
                "provider": "NASA",
                "resolution": "250m-1km",
                "temporal_coverage": "2000-present",
                "update_frequency": "Daily"
            }
        ],
        "processing_methods": [
            "NDVI (Normalized Difference Vegetation Index)",
            "Machine Learning Classification",
            "Change Detection Algorithms",
            "Cloud Masking and Atmospheric Correction"
        ],
        "accuracy": {
            "overall_accuracy": "85-92%",
            "forest_detection": "90-95%",
            "change_detection": "80-88%"
        }
    }