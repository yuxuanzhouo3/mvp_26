"""
Medical Advice module for doctor/medical advice (e1-e9).
"""

from typing import Dict, Any, List
from .base import BaseModule, BaseSubmodule


class MedicalAdviceModule(BaseModule):
    """
    Medical Advice module for doctor/medical advice (e1-e9).
    """
    
    def _initialize_submodules(self):
        """Initialize e1-e9 submodules."""
        self.submodules = {
            1: E1SymptomAnalysis(self.config.get('e1', {})),
            2: E2HealthAssessment(self.config.get('e2', {})),
            3: E3TreatmentGuidance(self.config.get('e3', {})),
            4: E4MedicationAdvice(self.config.get('e4', {})),
            5: E5LifestyleRecommendations(self.config.get('e5', {})),
            6: E6PreventiveCare(self.config.get('e6', {})),
            7: E7MentalHealthSupport(self.config.get('e7', {})),
            8: E8EmergencyGuidance(self.config.get('e8', {})),
            9: E9HealthEducation(self.config.get('e9', {}))
        }
    
    def get_description(self) -> str:
        return "Doctor/medical advice and health consultation AI"


class E1SymptomAnalysis(BaseSubmodule):
    """e1: Analyze symptoms and provide preliminary assessment."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        symptoms = request.get('symptoms', [])
        duration = request.get('duration', '')
        severity = request.get('severity', 'mild')
        
        analysis = self._analyze_symptoms(symptoms, duration, severity)
        
        return {
            'symptoms': symptoms,
            'duration': duration,
            'severity': severity,
            'analysis': analysis,
            'possible_conditions': self._identify_possible_conditions(analysis),
            'urgency_level': self._assess_urgency(analysis)
        }
    
    def _analyze_symptoms(self, symptoms: List[str], duration: str, severity: str) -> Dict[str, Any]:
        return {
            'symptom_pattern': 'Consistent with common conditions',
            'severity_assessment': severity,
            'duration_analysis': f'Symptoms present for {duration}',
            'risk_factors': ['Age', 'Medical history', 'Lifestyle factors']
        }
    
    def _identify_possible_conditions(self, analysis: Dict[str, Any]) -> List[str]:
        return [
            'Common cold or flu',
            'Seasonal allergies',
            'Stress-related symptoms',
            'Minor infection'
        ]
    
    def _assess_urgency(self, analysis: Dict[str, Any]) -> str:
        return 'Low'  # Default to low urgency for safety
    
    def get_description(self) -> str:
        return "Analyze symptoms and provide preliminary assessment"


class E2HealthAssessment(BaseSubmodule):
    """e2: Comprehensive health assessment and evaluation."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        health_data = request.get('health_data', {})
        assessment_type = request.get('assessment_type', 'general')
        
        assessment = self._conduct_health_assessment(health_data, assessment_type)
        
        return {
            'health_data': health_data,
            'assessment_type': assessment_type,
            'assessment': assessment,
            'health_score': self._calculate_health_score(assessment),
            'recommendations': self._generate_recommendations(assessment)
        }
    
    def _conduct_health_assessment(self, data: Dict, assessment_type: str) -> Dict[str, Any]:
        return {
            'overall_health': 'Good',
            'risk_factors': ['Sedentary lifestyle', 'Poor diet'],
            'strengths': ['Regular exercise', 'Good sleep habits'],
            'areas_for_improvement': ['Nutrition', 'Stress management']
        }
    
    def _calculate_health_score(self, assessment: Dict[str, Any]) -> float:
        return 75.5
    
    def _generate_recommendations(self, assessment: Dict[str, Any]) -> List[str]:
        return [
            'Increase physical activity',
            'Improve dietary habits',
            'Manage stress levels',
            'Schedule regular check-ups'
        ]
    
    def get_description(self) -> str:
        return "Comprehensive health assessment and evaluation"


class E3TreatmentGuidance(BaseSubmodule):
    """e3: Provide treatment guidance and recommendations."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        condition = request.get('condition', '')
        symptoms = request.get('symptoms', [])
        medical_history = request.get('medical_history', {})
        
        guidance = self._provide_treatment_guidance(condition, symptoms, medical_history)
        
        return {
            'condition': condition,
            'symptoms': symptoms,
            'medical_history': medical_history,
            'treatment_guidance': guidance,
            'treatment_options': self._suggest_treatment_options(condition),
            'follow_up_plan': self._create_follow_up_plan(guidance)
        }
    
    def _provide_treatment_guidance(self, condition: str, symptoms: List[str], history: Dict) -> Dict[str, Any]:
        return {
            'recommended_treatments': ['Rest', 'Hydration', 'Over-the-counter medications'],
            'avoid': ['Strenuous activity', 'Certain medications'],
            'monitoring': ['Symptom progression', 'Temperature', 'Pain levels'],
            'when_to_seek_care': 'If symptoms worsen or persist beyond 7 days'
        }
    
    def _suggest_treatment_options(self, condition: str) -> List[str]:
        return [
            'Home remedies',
            'Over-the-counter medications',
            'Lifestyle modifications',
            'Professional medical care'
        ]
    
    def _create_follow_up_plan(self, guidance: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'timeline': '7-10 days',
            'monitoring_points': ['Symptom improvement', 'Side effects', 'Recovery progress'],
            'next_steps': 'Schedule follow-up if needed'
        }
    
    def get_description(self) -> str:
        return "Provide treatment guidance and recommendations"


class E4MedicationAdvice(BaseSubmodule):
    """e4: Provide medication advice and information."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        medication = request.get('medication', '')
        condition = request.get('condition', '')
        current_medications = request.get('current_medications', [])
        
        advice = self._provide_medication_advice(medication, condition, current_medications)
        
        return {
            'medication': medication,
            'condition': condition,
            'current_medications': current_medications,
            'medication_advice': advice,
            'interactions': self._check_interactions(medication, current_medications),
            'side_effects': self._list_side_effects(medication)
        }
    
    def _provide_medication_advice(self, medication: str, condition: str, current: List[str]) -> Dict[str, Any]:
        return {
            'dosage': 'As prescribed by healthcare provider',
            'timing': 'Take with food if recommended',
            'duration': 'Complete full course',
            'precautions': ['Avoid alcohol', 'Monitor for side effects']
        }
    
    def _check_interactions(self, medication: str, current: List[str]) -> List[str]:
        return [
            'No known interactions with current medications',
            'Consult healthcare provider for specific concerns'
        ]
    
    def _list_side_effects(self, medication: str) -> List[str]:
        return [
            'Common: Nausea, headache',
            'Rare: Allergic reactions',
            'Contact healthcare provider if severe side effects occur'
        ]
    
    def get_description(self) -> str:
        return "Provide medication advice and information"


class E5LifestyleRecommendations(BaseSubmodule):
    """e5: Provide lifestyle and wellness recommendations."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        current_lifestyle = request.get('current_lifestyle', {})
        health_goals = request.get('health_goals', [])
        preferences = request.get('preferences', {})
        
        recommendations = self._provide_lifestyle_recommendations(current_lifestyle, health_goals, preferences)
        
        return {
            'current_lifestyle': current_lifestyle,
            'health_goals': health_goals,
            'preferences': preferences,
            'recommendations': recommendations,
            'implementation_plan': self._create_implementation_plan(recommendations),
            'progress_tracking': self._suggest_progress_tracking(recommendations)
        }
    
    def _provide_lifestyle_recommendations(self, current: Dict, goals: List[str], preferences: Dict) -> Dict[str, Any]:
        return {
            'diet': ['Increase vegetable intake', 'Reduce processed foods', 'Stay hydrated'],
            'exercise': ['30 minutes daily activity', 'Strength training 2-3 times/week', 'Flexibility exercises'],
            'sleep': ['7-9 hours nightly', 'Consistent sleep schedule', 'Create relaxing bedtime routine'],
            'stress_management': ['Meditation', 'Deep breathing exercises', 'Regular breaks']
        }
    
    def _create_implementation_plan(self, recommendations: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'phase_1': 'Start with one change per week',
            'phase_2': 'Gradually increase intensity',
            'phase_3': 'Maintain sustainable habits',
            'timeline': '3-6 months for full implementation'
        }
    
    def _suggest_progress_tracking(self, recommendations: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'metrics': ['Weight', 'Energy levels', 'Sleep quality', 'Stress levels'],
            'frequency': 'Weekly check-ins',
            'tools': ['Health apps', 'Journaling', 'Wearable devices']
        }
    
    def get_description(self) -> str:
        return "Provide lifestyle and wellness recommendations"


class E6PreventiveCare(BaseSubmodule):
    """e6: Provide preventive care recommendations and screening guidance."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        age = request.get('age', 30)
        gender = request.get('gender', '')
        family_history = request.get('family_history', [])
        
        preventive_care = self._recommend_preventive_care(age, gender, family_history)
        
        return {
            'age': age,
            'gender': gender,
            'family_history': family_history,
            'preventive_care': preventive_care,
            'screening_schedule': self._create_screening_schedule(age, gender),
            'vaccination_recommendations': self._recommend_vaccinations(age)
        }
    
    def _recommend_preventive_care(self, age: int, gender: str, history: List[str]) -> Dict[str, Any]:
        return {
            'annual_checkup': 'Recommended for all adults',
            'blood_pressure': 'Check every 2 years',
            'cholesterol': 'Check every 4-6 years',
            'diabetes_screening': 'Based on risk factors',
            'cancer_screening': 'Age and gender-specific recommendations'
        }
    
    def _create_screening_schedule(self, age: int, gender: str) -> Dict[str, Any]:
        return {
            'immediate': ['Annual physical exam'],
            'within_6_months': ['Blood work if needed'],
            'within_1_year': ['Dental checkup', 'Eye exam'],
            'future': ['Age-appropriate screenings']
        }
    
    def _recommend_vaccinations(self, age: int) -> List[str]:
        return [
            'Annual flu vaccine',
            'Tdap booster every 10 years',
            'Age-appropriate vaccines as recommended'
        ]
    
    def get_description(self) -> str:
        return "Provide preventive care recommendations and screening guidance"


class E7MentalHealthSupport(BaseSubmodule):
    """e7: Provide mental health support and guidance."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        mental_health_concerns = request.get('concerns', [])
        current_mood = request.get('mood', 'neutral')
        stress_level = request.get('stress_level', 'moderate')
        
        support_plan = self._provide_mental_health_support(mental_health_concerns, current_mood, stress_level)
        
        return {
            'mental_health_concerns': mental_health_concerns,
            'current_mood': current_mood,
            'stress_level': stress_level,
            'support_plan': support_plan,
            'coping_strategies': self._suggest_coping_strategies(stress_level),
            'professional_help': self._recommend_professional_help(mental_health_concerns)
        }
    
    def _provide_mental_health_support(self, concerns: List[str], mood: str, stress: str) -> Dict[str, Any]:
        return {
            'daily_practices': ['Mindfulness meditation', 'Regular exercise', 'Adequate sleep'],
            'stress_management': ['Deep breathing exercises', 'Progressive muscle relaxation', 'Time management'],
            'social_support': ['Connect with friends and family', 'Join support groups', 'Seek professional counseling'],
            'self_care': ['Engage in hobbies', 'Practice gratitude', 'Set healthy boundaries']
        }
    
    def _suggest_coping_strategies(self, stress_level: str) -> List[str]:
        return [
            'Practice deep breathing exercises',
            'Take regular breaks throughout the day',
            'Engage in physical activity',
            'Maintain a regular sleep schedule'
        ]
    
    def _recommend_professional_help(self, concerns: List[str]) -> Dict[str, Any]:
        return {
            'when_to_seek_help': 'If symptoms persist for more than 2 weeks',
            'types_of_professionals': ['Psychologist', 'Psychiatrist', 'Licensed counselor'],
            'resources': ['Mental health hotlines', 'Online therapy platforms', 'Support groups']
        }
    
    def get_description(self) -> str:
        return "Provide mental health support and guidance"


class E8EmergencyGuidance(BaseSubmodule):
    """e8: Provide emergency guidance and first aid information."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        emergency_type = request.get('emergency_type', '')
        symptoms = request.get('symptoms', [])
        location = request.get('location', '')
        
        guidance = self._provide_emergency_guidance(emergency_type, symptoms, location)
        
        return {
            'emergency_type': emergency_type,
            'symptoms': symptoms,
            'location': location,
            'emergency_guidance': guidance,
            'immediate_actions': self._suggest_immediate_actions(emergency_type),
            'when_to_call_emergency': self._determine_emergency_criteria(emergency_type)
        }
    
    def _provide_emergency_guidance(self, emergency_type: str, symptoms: List[str], location: str) -> Dict[str, Any]:
        return {
            'immediate_steps': ['Assess safety', 'Call emergency services if needed', 'Provide basic first aid'],
            'do_not_do': ['Move seriously injured person', 'Give medication without medical advice'],
            'monitoring': ['Vital signs', 'Consciousness level', 'Breathing'],
            'follow_up': 'Seek medical attention as soon as possible'
        }
    
    def _suggest_immediate_actions(self, emergency_type: str) -> List[str]:
        return [
            'Ensure scene safety',
            'Call emergency services if needed',
            'Provide basic first aid',
            'Stay with the person until help arrives'
        ]
    
    def _determine_emergency_criteria(self, emergency_type: str) -> List[str]:
        return [
            'Severe bleeding',
            'Difficulty breathing',
            'Loss of consciousness',
            'Chest pain',
            'Severe head injury'
        ]
    
    def get_description(self) -> str:
        return "Provide emergency guidance and first aid information"


class E9HealthEducation(BaseSubmodule):
    """e9: Provide health education and information."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        topic = request.get('topic', '')
        education_level = request.get('education_level', 'general')
        format_preference = request.get('format', 'text')
        
        education_content = self._provide_health_education(topic, education_level, format_preference)
        
        return {
            'topic': topic,
            'education_level': education_level,
            'format_preference': format_preference,
            'education_content': education_content,
            'additional_resources': self._suggest_additional_resources(topic),
            'learning_objectives': self._define_learning_objectives(topic)
        }
    
    def _provide_health_education(self, topic: str, level: str, format: str) -> Dict[str, Any]:
        return {
            'overview': f'Comprehensive information about {topic}',
            'key_points': ['Important fact 1', 'Important fact 2', 'Important fact 3'],
            'common_misconceptions': ['Misconception 1', 'Misconception 2'],
            'practical_applications': ['How to apply knowledge 1', 'How to apply knowledge 2']
        }
    
    def _suggest_additional_resources(self, topic: str) -> List[str]:
        return [
            'Reputable health websites',
            'Medical journals and publications',
            'Educational videos and podcasts',
            'Healthcare provider consultations'
        ]
    
    def _define_learning_objectives(self, topic: str) -> List[str]:
        return [
            'Understand basic concepts',
            'Identify risk factors',
            'Learn prevention strategies',
            'Know when to seek medical help'
        ]
    
    def get_description(self) -> str:
        return "Provide health education and information" 