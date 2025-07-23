"""
Personalized Traveling module for travel planning and cultural insights.
"""

from typing import Dict, Any
from .base import BaseModule, BaseSubmodule


class R1TravelPlanning(BaseSubmodule):
    """Create personalized travel itineraries and planning advice."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process travel planning request."""
        destination = request.get('destination', '')
        duration = request.get('duration', 7)
        budget = request.get('budget', 'medium')
        travel_style = request.get('travel_style', 'balanced')
        interests = request.get('interests', [])
        
        return {
            'travel_itinerary': {
                'day_1': {
                    'morning': 'Arrival and hotel check-in',
                    'afternoon': 'City orientation tour',
                    'evening': 'Welcome dinner at local restaurant',
                    'accommodation': 'Downtown hotel'
                },
                'day_2': {
                    'morning': 'Historical sites visit',
                    'afternoon': 'Local market exploration',
                    'evening': 'Cultural performance',
                    'accommodation': 'Downtown hotel'
                },
                'day_3': {
                    'morning': 'Museum visits',
                    'afternoon': 'Shopping district',
                    'evening': 'Rooftop bar experience',
                    'accommodation': 'Downtown hotel'
                }
            },
            'budget_breakdown': {
                'accommodation': '$800 (40%)',
                'transportation': '$400 (20%)',
                'food': '$500 (25%)',
                'activities': '$300 (15%)'
            },
            'planning_tips': [
                'Book flights 2-3 months in advance',
                'Reserve popular attractions early',
                'Pack light and versatile clothing',
                'Learn basic local phrases',
                'Download offline maps'
            ],
            'travel_style_recommendations': {
                'budget': 'Hostels, public transport, street food',
                'balanced': 'Mid-range hotels, mix of transport, local restaurants',
                'luxury': 'High-end hotels, private transport, fine dining'
            }
        }
    
    def get_description(self) -> str:
        return "Create personalized travel itineraries and planning advice"


class R2TransportationAdvice(BaseSubmodule):
    """Provide transportation recommendations from point A to B."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process transportation advice request."""
        origin = request.get('origin', '')
        destination = request.get('destination', '')
        date = request.get('date', '')
        passengers = request.get('passengers', 1)
        preferences = request.get('preferences', {})
        
        return {
            'transportation_options': [
                {
                    'mode': 'Flight',
                    'duration': '2h 15m',
                    'cost': 180,
                    'airline': 'Delta Airlines',
                    'departure': '10:30 AM',
                    'arrival': '12:45 PM',
                    'booking_links': {
                        'expedia': 'https://expedia.com/flight-1',
                        'kayak': 'https://kayak.com/flight-1',
                        'google_flights': 'https://google.com/flights/flight-1'
                    }
                },
                {
                    'mode': 'Train',
                    'duration': '4h 30m',
                    'cost': 85,
                    'operator': 'Amtrak',
                    'departure': '8:00 AM',
                    'arrival': '12:30 PM',
                    'booking_links': {
                        'amtrak': 'https://amtrak.com/train-1',
                        'trainline': 'https://trainline.com/train-1'
                    }
                },
                {
                    'mode': 'Bus',
                    'duration': '6h 15m',
                    'cost': 45,
                    'operator': 'Greyhound',
                    'departure': '7:00 AM',
                    'arrival': '1:15 PM',
                    'booking_links': {
                        'greyhound': 'https://greyhound.com/bus-1',
                        'megabus': 'https://megabus.com/bus-1'
                    }
                },
                {
                    'mode': 'Car Rental',
                    'duration': '3h 45m',
                    'cost': 120,
                    'operator': 'Enterprise',
                    'fuel_cost': 35,
                    'booking_links': {
                        'enterprise': 'https://enterprise.com/car-1',
                        'hertz': 'https://hertz.com/car-1',
                        'avis': 'https://avis.com/car-1'
                    }
                }
            ],
            'recommendations': {
                'fastest': 'Flight - 2h 15m',
                'cheapest': 'Bus - $45',
                'most_scenic': 'Train - 4h 30m',
                'most_flexible': 'Car Rental - 3h 45m'
            },
            'local_transportation': {
                'public_transit': {
                    'metro': 'Efficient subway system, $2.75 per ride',
                    'bus': 'Comprehensive network, $2.75 per ride',
                    'passes': '7-day pass for $33'
                },
                'ride_sharing': {
                    'uber': 'Widely available, 5-10 min wait',
                    'lyft': 'Good coverage, similar pricing',
                    'local_taxis': 'Available but more expensive'
                },
                'bike_sharing': {
                    'citibike': '$3.50 per 30 min',
                    'lime': '$1 to unlock + $0.15/min'
                }
            }
        }
    
    def get_description(self) -> str:
        return "Provide transportation recommendations from point A to B"


class R3CulturalInsights(BaseSubmodule):
    """Provide cultural insights and local customs information."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process cultural insights request."""
        destination = request.get('destination', '')
        focus_areas = request.get('focus_areas', ['customs', 'food', 'language'])
        
        return {
            'cultural_overview': {
                'language': {
                    'primary': 'English',
                    'common_phrases': [
                        'Hello - Hi',
                        'Thank you - Thanks',
                        'Goodbye - Bye',
                        'Please - Please',
                        'Excuse me - Excuse me'
                    ],
                    'language_tips': 'English is widely spoken, but learning basic phrases shows respect'
                },
                'customs': {
                    'greetings': 'Handshakes are common, hugs for close friends',
                    'dining': 'Tip 15-20% at restaurants, wait to be seated',
                    'dress_code': 'Casual in most places, business casual for work',
                    'punctuality': 'Being on time is important, especially for business'
                },
                'etiquette': [
                    'Say "please" and "thank you" frequently',
                    'Hold doors open for others',
                    'Don\'t talk loudly in public spaces',
                    'Respect personal space',
                    'Follow local laws and customs'
                ]
            },
            'local_culture': {
                'food_culture': {
                    'dining_times': 'Breakfast 7-9 AM, Lunch 12-2 PM, Dinner 6-8 PM',
                    'tipping': '15-20% at restaurants, $1-2 for coffee',
                    'local_specialties': ['Pizza', 'Burgers', 'BBQ', 'Seafood'],
                    'dietary_considerations': 'Vegetarian and vegan options widely available'
                },
                'social_customs': {
                    'personal_space': 'Arm\'s length distance when talking',
                    'eye_contact': 'Maintain eye contact during conversations',
                    'gift_giving': 'Not expected but appreciated, avoid expensive gifts',
                    'business_culture': 'Direct communication, punctuality important'
                }
            },
            'cultural_activities': [
                'Visit local museums and galleries',
                'Attend cultural festivals and events',
                'Take cooking classes to learn local cuisine',
                'Join guided cultural tours',
                'Participate in local community events'
            ]
        }
    
    def get_description(self) -> str:
        return "Provide cultural insights and local customs information"


class R4AccommodationBooking(BaseSubmodule):
    """Provide accommodation recommendations and booking assistance."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process accommodation booking request."""
        destination = request.get('destination', '')
        dates = request.get('dates', {})
        guests = request.get('guests', 2)
        budget = request.get('budget', 'medium')
        preferences = request.get('preferences', {})
        
        return {
            'accommodation_options': [
                {
                    'name': 'The Grand Hotel',
                    'type': 'Luxury Hotel',
                    'rating': 4.8,
                    'price_per_night': 350,
                    'amenities': ['Spa', 'Pool', 'Restaurant', 'Gym', 'Concierge'],
                    'location': 'Downtown',
                    'booking_links': {
                        'booking': 'https://booking.com/grand-hotel',
                        'expedia': 'https://expedia.com/grand-hotel',
                        'hotels': 'https://hotels.com/grand-hotel'
                    }
                },
                {
                    'name': 'Cozy Boutique Inn',
                    'type': 'Boutique Hotel',
                    'rating': 4.5,
                    'price_per_night': 180,
                    'amenities': ['Free WiFi', 'Breakfast', 'Garden', 'Local tours'],
                    'location': 'Historic District',
                    'booking_links': {
                        'booking': 'https://booking.com/boutique-inn',
                        'expedia': 'https://expedia.com/boutique-inn',
                        'hotels': 'https://hotels.com/boutique-inn'
                    }
                },
                {
                    'name': 'Downtown Hostel',
                    'type': 'Hostel',
                    'rating': 4.2,
                    'price_per_night': 45,
                    'amenities': ['Shared kitchen', 'Common room', 'Free WiFi', 'Laundry'],
                    'location': 'Downtown',
                    'booking_links': {
                        'hostelworld': 'https://hostelworld.com/downtown-hostel',
                        'booking': 'https://booking.com/downtown-hostel'
                    }
                },
                {
                    'name': 'Luxury Vacation Rental',
                    'type': 'Vacation Rental',
                    'rating': 4.7,
                    'price_per_night': 250,
                    'amenities': ['Full kitchen', 'Private balcony', 'Washing machine', 'Parking'],
                    'location': 'Residential Area',
                    'booking_links': {
                        'airbnb': 'https://airbnb.com/vacation-rental',
                        'vrbo': 'https://vrbo.com/vacation-rental'
                    }
                }
            ],
            'accommodation_tips': [
                'Book 2-3 months in advance for popular destinations',
                'Check cancellation policies before booking',
                'Read recent reviews for current conditions',
                'Consider location vs. price trade-offs',
                'Look for package deals with flights'
            ],
            'accommodation_types': {
                'hotels': {
                    'pros': ['Convenient', 'Amenities', 'Concierge service'],
                    'cons': ['More expensive', 'Less local experience'],
                    'best_for': 'Business travel, luxury, convenience'
                },
                'hostels': {
                    'pros': ['Budget-friendly', 'Social atmosphere', 'Local tips'],
                    'cons': ['Shared facilities', 'Less privacy'],
                    'best_for': 'Budget travel, solo travelers, social experience'
                },
                'vacation_rentals': {
                    'pros': ['More space', 'Kitchen facilities', 'Local experience'],
                    'cons': ['Less service', 'Variable quality'],
                    'best_for': 'Families, longer stays, local experience'
                }
            }
        }
    
    def get_description(self) -> str:
        return "Provide accommodation recommendations and booking assistance"


class R5LocalAttractions(BaseSubmodule):
    """Recommend local attractions and must-see destinations."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process local attractions request."""
        destination = request.get('destination', '')
        interests = request.get('interests', ['culture', 'food', 'nature'])
        duration = request.get('duration', 3)
        budget = request.get('budget', 'medium')
        
        return {
            'top_attractions': [
                {
                    'name': 'Historic Downtown',
                    'type': 'Cultural',
                    'rating': 4.8,
                    'duration': 'Half day',
                    'cost': 'Free',
                    'highlights': ['Architecture', 'History', 'Shopping'],
                    'tips': 'Visit early morning for fewer crowds',
                    'booking_links': {
                        'viator': 'https://viator.com/historic-downtown',
                        'getyourguide': 'https://getyourguide.com/historic-downtown'
                    }
                },
                {
                    'name': 'Local Food Market',
                    'type': 'Food & Culture',
                    'rating': 4.6,
                    'duration': '2-3 hours',
                    'cost': '$20-50',
                    'highlights': ['Local cuisine', 'Fresh produce', 'Street food'],
                    'tips': 'Go hungry and try multiple vendors',
                    'booking_links': {
                        'viator': 'https://viator.com/food-market',
                        'airbnb_experiences': 'https://airbnb.com/experiences/food-market'
                    }
                },
                {
                    'name': 'City Park',
                    'type': 'Nature',
                    'rating': 4.5,
                    'duration': '2-4 hours',
                    'cost': 'Free',
                    'highlights': ['Walking trails', 'Scenic views', 'Wildlife'],
                    'tips': 'Best visited during golden hour',
                    'booking_links': {
                        'viator': 'https://viator.com/city-park',
                        'getyourguide': 'https://getyourguide.com/city-park'
                    }
                }
            ],
            'hidden_gems': [
                {
                    'name': 'Local Art Gallery',
                    'description': 'Small gallery featuring local artists',
                    'cost': 'Free',
                    'location': 'Arts District'
                },
                {
                    'name': 'Rooftop Garden',
                    'description': 'Peaceful garden with city views',
                    'cost': '$5',
                    'location': 'Downtown'
                },
                {
                    'name': 'Historic Library',
                    'description': 'Beautiful architecture and quiet reading spaces',
                    'cost': 'Free',
                    'location': 'University District'
                }
            ],
            'seasonal_attractions': {
                'spring': ['Cherry blossom festival', 'Spring markets', 'Outdoor concerts'],
                'summer': ['Beach activities', 'Summer festivals', 'Outdoor dining'],
                'fall': ['Fall foliage tours', 'Harvest festivals', 'Wine tastings'],
                'winter': ['Holiday markets', 'Ice skating', 'Indoor museums']
            },
            'attraction_tips': [
                'Buy tickets online to avoid lines',
                'Visit popular attractions early or late',
                'Check for free admission days',
                'Consider city passes for multiple attractions',
                'Ask locals for recommendations'
            ]
        }
    
    def get_description(self) -> str:
        return "Recommend local attractions and must-see destinations"


class R6TravelInsurance(BaseSubmodule):
    """Provide travel insurance advice and recommendations."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process travel insurance request."""
        trip_details = request.get('trip_details', {})
        destination = request.get('destination', '')
        duration = request.get('duration', 7)
        activities = request.get('activities', [])
        travelers = request.get('travelers', 1)
        
        return {
            'insurance_recommendations': [
                {
                    'provider': 'World Nomads',
                    'plan': 'Standard Plan',
                    'coverage': {
                        'medical': '$100,000',
                        'evacuation': '$300,000',
                        'trip_cancellation': '$10,000',
                        'baggage': '$1,000'
                    },
                    'cost': 45,
                    'rating': 4.7,
                    'website': 'https://worldnomads.com'
                },
                {
                    'provider': 'Allianz',
                    'plan': 'OneTrip Prime',
                    'coverage': {
                        'medical': '$50,000',
                        'evacuation': '$500,000',
                        'trip_cancellation': '$100,000',
                        'baggage': '$1,000'
                    },
                    'cost': 52,
                    'rating': 4.5,
                    'website': 'https://allianztravelinsurance.com'
                },
                {
                    'provider': 'Travel Guard',
                    'plan': 'Deluxe Plan',
                    'coverage': {
                        'medical': '$50,000',
                        'evacuation': '$500,000',
                        'trip_cancellation': '$100,000',
                        'baggage': '$1,000'
                    },
                    'cost': 48,
                    'rating': 4.3,
                    'website': 'https://travelguard.com'
                }
            ],
            'coverage_types': {
                'medical': 'Covers medical expenses and emergency care',
                'evacuation': 'Covers emergency evacuation to home country',
                'trip_cancellation': 'Covers non-refundable trip costs',
                'baggage': 'Covers lost, stolen, or damaged luggage',
                'flight_delay': 'Covers expenses due to flight delays',
                'rental_car': 'Covers rental car damage and liability'
            },
            'when_to_buy': {
                'trip_cancellation': 'As soon as you book non-refundable expenses',
                'medical': 'Before departure',
                'baggage': 'Before departure',
                'activities': 'Before participating in adventure activities'
            },
            'insurance_tips': [
                'Read the fine print carefully',
                'Check what\'s not covered',
                'Consider your health and activities',
                'Compare multiple providers',
                'Keep insurance documents accessible'
            ]
        }
    
    def get_description(self) -> str:
        return "Provide travel insurance advice and recommendations"


class R7PackingGuidance(BaseSubmodule):
    """Provide packing advice and checklist recommendations."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process packing guidance request."""
        destination = request.get('destination', '')
        duration = request.get('duration', 7)
        climate = request.get('climate', 'temperate')
        activities = request.get('activities', [])
        luggage_type = request.get('luggage_type', 'checked')
        
        return {
            'packing_checklist': {
                'clothing': [
                    'Underwear (1 per day + 2 extra)',
                    'Socks (1 per day + 2 extra)',
                    'T-shirts/tops (1 per day)',
                    'Pants/shorts (1 per 2 days)',
                    'Dress/formal outfit (if needed)',
                    'Pajamas',
                    'Swimwear (if applicable)',
                    'Outerwear (jacket/sweater)'
                ],
                'toiletries': [
                    'Toothbrush and toothpaste',
                    'Shampoo and conditioner',
                    'Soap or body wash',
                    'Deodorant',
                    'Hair care products',
                    'Skincare products',
                    'Razor and shaving cream',
                    'Feminine hygiene products (if needed)'
                ],
                'electronics': [
                    'Phone and charger',
                    'Camera and memory cards',
                    'Power bank',
                    'Universal adapter (if international)',
                    'Laptop/tablet (if needed)',
                    'Headphones'
                ],
                'documents': [
                    'Passport (if international)',
                    'Driver\'s license',
                    'Credit cards',
                    'Travel insurance documents',
                    'Boarding passes',
                    'Hotel confirmations',
                    'Emergency contacts'
                ],
                'accessories': [
                    'Sunglasses',
                    'Hat or cap',
                    'Scarf or gloves (if cold)',
                    'Umbrella or rain jacket',
                    'Day bag or backpack',
                    'Water bottle',
                    'Snacks'
                ]
            },
            'climate_specific_packing': {
                'tropical': [
                    'Light, breathable clothing',
                    'Sunscreen and hat',
                    'Insect repellent',
                    'Quick-dry clothing',
                    'Waterproof bag'
                ],
                'cold': [
                    'Layered clothing',
                    'Warm jacket and gloves',
                    'Thermal underwear',
                    'Warm socks and boots',
                    'Hand warmers'
                ],
                'temperate': [
                    'Layered clothing',
                    'Light jacket',
                    'Comfortable walking shoes',
                    'Umbrella',
                    'Versatile clothing'
                ]
            },
            'packing_tips': [
                'Roll clothes to save space',
                'Use packing cubes for organization',
                'Pack heavy items at the bottom',
                'Keep essentials in carry-on',
                'Check airline baggage restrictions',
                'Leave room for souvenirs'
            ],
            'luggage_recommendations': {
                'carry_on': {
                    'size': '22" x 14" x 9"',
                    'weight_limit': '7-10 kg',
                    'best_for': 'Short trips, business travel'
                },
                'checked': {
                    'size': '28" x 20" x 12"',
                    'weight_limit': '23 kg',
                    'best_for': 'Longer trips, families'
                }
            }
        }
    
    def get_description(self) -> str:
        return "Provide packing advice and checklist recommendations"


class R8SafetyAdvice(BaseSubmodule):
    """Provide travel safety advice and emergency information."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process safety advice request."""
        destination = request.get('destination', '')
        travel_type = request.get('travel_type', 'leisure')
        solo_travel = request.get('solo_travel', False)
        
        return {
            'safety_overview': {
                'overall_safety': 'Generally safe for tourists',
                'crime_level': 'Low to moderate',
                'health_risks': 'Minimal',
                'political_stability': 'Stable'
            },
            'safety_tips': {
                'general': [
                    'Keep copies of important documents',
                    'Don\'t carry all cash in one place',
                    'Be aware of your surroundings',
                    'Trust your instincts',
                    'Learn basic local phrases'
                ],
                'transportation': [
                    'Use official taxi services',
                    'Avoid unmarked vehicles',
                    'Keep valuables close on public transport',
                    'Be cautious at night',
                    'Share your location with trusted contacts'
                ],
                'accommodation': [
                    'Choose well-reviewed accommodations',
                    'Lock doors and windows',
                    'Use hotel safe for valuables',
                    'Keep emergency contacts handy',
                    'Know emergency exits'
                ]
            },
            'emergency_contacts': {
                'local_emergency': '911',
                'police': '911',
                'ambulance': '911',
                'fire': '911',
                'us_embassy': '+1-202-501-4444',
                'local_hospital': 'Main Hospital: +1-555-123-4567'
            },
            'health_safety': {
                'vaccinations': 'Routine vaccinations recommended',
                'water_safety': 'Tap water is generally safe',
                'food_safety': 'Eat at busy restaurants, avoid street food if sensitive',
                'medical_facilities': 'Good medical care available in major cities'
            },
            'solo_travel_safety': [
                'Stay in well-lit, populated areas',
                'Avoid walking alone at night',
                'Share your itinerary with family/friends',
                'Join group tours for certain activities',
                'Trust your gut feeling about situations'
            ],
            'scam_awareness': [
                'Beware of overly friendly strangers',
                'Don\'t accept unsolicited help',
                'Verify prices before agreeing',
                'Be cautious of "free" offers',
                'Use official booking sites'
            ]
        }
    
    def get_description(self) -> str:
        return "Provide travel safety advice and emergency information"


class R9TravelIntegration(BaseSubmodule):
    """Integrate with multiple travel platforms and provide booking links."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process travel integration request."""
        travel_type = request.get('type', 'flights')
        destination = request.get('destination', '')
        dates = request.get('dates', {})
        
        return {
            'platform_integration': {
                'flights': {
                    'google_flights': {
                        'availability': True,
                        'price_tracking': True,
                        'flexible_dates': True,
                        'mobile_app': True
                    },
                    'skyscanner': {
                        'availability': True,
                        'price_tracking': True,
                        'flexible_dates': True,
                        'mobile_app': True
                    },
                    'kayak': {
                        'availability': True,
                        'price_tracking': True,
                        'flexible_dates': True,
                        'mobile_app': True
                    },
                    'expedia': {
                        'availability': True,
                        'price_tracking': True,
                        'package_deals': True,
                        'mobile_app': True
                    }
                },
                'accommodation': {
                    'booking': {
                        'availability': True,
                        'best_price_guarantee': True,
                        'loyalty_program': True,
                        'mobile_app': True
                    },
                    'airbnb': {
                        'availability': True,
                        'unique_stays': True,
                        'local_experiences': True,
                        'mobile_app': True
                    },
                    'hotels': {
                        'availability': True,
                        'best_price_guarantee': True,
                        'loyalty_program': True,
                        'mobile_app': True
                    }
                },
                'activities': {
                    'viator': {
                        'availability': True,
                        'guided_tours': True,
                        'skip_the_line': True,
                        'mobile_app': True
                    },
                    'getyourguide': {
                        'availability': True,
                        'local_experiences': True,
                        'flexible_cancellation': True,
                        'mobile_app': True
                    },
                    'airbnb_experiences': {
                        'availability': True,
                        'unique_activities': True,
                        'local_hosts': True,
                        'mobile_app': True
                    }
                },
                'transportation': {
                    'uber': {
                        'availability': True,
                        'ride_sharing': True,
                        'food_delivery': True,
                        'mobile_app': True
                    },
                    'lyft': {
                        'availability': True,
                        'ride_sharing': True,
                        'bike_sharing': True,
                        'mobile_app': True
                    },
                    'rental_cars': {
                        'enterprise': 'https://enterprise.com',
                        'hertz': 'https://hertz.com',
                        'avis': 'https://avis.com'
                    }
                }
            },
            'order_links': {
                'flights': {
                    'google_flights': 'https://google.com/flights',
                    'skyscanner': 'https://skyscanner.com',
                    'kayak': 'https://kayak.com',
                    'expedia': 'https://expedia.com'
                },
                'accommodation': {
                    'booking': 'https://booking.com',
                    'airbnb': 'https://airbnb.com',
                    'hotels': 'https://hotels.com'
                },
                'activities': {
                    'viator': 'https://viator.com',
                    'getyourguide': 'https://getyourguide.com',
                    'airbnb_experiences': 'https://airbnb.com/experiences'
                },
                'transportation': {
                    'uber': 'https://uber.com',
                    'lyft': 'https://lyft.com'
                }
            },
            'popularity_rankings': [
                {'platform': 'Google Flights', 'score': 9.4, 'reasons': ['Best prices', 'Easy interface', 'Price tracking']},
                {'platform': 'Booking.com', 'score': 9.2, 'reasons': ['Wide selection', 'Good prices', 'Reliable']},
                {'platform': 'Airbnb', 'score': 8.9, 'reasons': ['Unique stays', 'Local experience', 'Good for groups']},
                {'platform': 'Viator', 'score': 8.7, 'reasons': ['Quality tours', 'Skip-the-line options', 'Good guides']},
                {'platform': 'Uber', 'score': 8.5, 'reasons': ['Widely available', 'Reliable', 'Good app']}
            ],
            'recommendations': {
                'best_flights': 'Google Flights',
                'best_hotels': 'Booking.com',
                'best_unique_stays': 'Airbnb',
                'best_activities': 'Viator',
                'best_transportation': 'Uber',
                'best_packages': 'Expedia'
            }
        }
    
    def get_description(self) -> str:
        return "Integrate with multiple travel platforms and provide booking links"


class PersonalizedTravelingModule(BaseModule):
    """Personalized Traveling module for travel planning and cultural insights."""
    
    def _initialize_submodules(self):
        """Initialize traveling submodules."""
        self.submodules = {
            1: R1TravelPlanning(self.config.get('travel_planning', {})),
            2: R2TransportationAdvice(self.config.get('transportation_advice', {})),
            3: R3CulturalInsights(self.config.get('cultural_insights', {})),
            4: R4AccommodationBooking(self.config.get('accommodation_booking', {})),
            5: R5LocalAttractions(self.config.get('local_attractions', {})),
            6: R6TravelInsurance(self.config.get('travel_insurance', {})),
            7: R7PackingGuidance(self.config.get('packing_guidance', {})),
            8: R8SafetyAdvice(self.config.get('safety_advice', {})),
            9: R9TravelIntegration(self.config.get('travel_integration', {}))
        }
    
    def get_description(self) -> str:
        return "Personalized traveling advice with transportation, cultural insights, and booking integration" 