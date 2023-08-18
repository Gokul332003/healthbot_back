from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.chat.util import Chat, reflections
import re
import random
from gtts import gTTS
import base64

app = Flask(__name__)
CORS(app) 

# Define pairs of user inputs and bot responses
pairs = [
    [
        r"(.*)Who created you(.*)",
        ["I was created by the AI specialist GOKUL P",]
    ],
    [
        r"(.*)Yes(.*)",
        ["Please elaborate the details",]
    ],
    [
        r"(.*)sure(.*)",
        ["Please elaborate the details",]
    ],
    [
        r"(.*)connect to doctor(.*)",
        ["Sure.Please wait while I connect with one of our specialists...",]
    ],
    [
        r"(.*)talk to doctor(.*)",
        ["Sure.Please wait while I connect with one of our specialists...",]
    ],
    [
        r"(.*)speak to doctor(.*)",
        ["Sure.Please wait while I connect with one of our specialists...",]
    ],
    [
        r"(.*)tired(.*)",
        ["Feeling tired could be due to various factors such as inadequate sleep, stress, or an underlying health condition. Can you provide more details about your daily routine?",]
    ],
    [
        r"(.*)sleepy(.*)",
        ["Getting enough sleep is essential for your overall well-being. Aim for 7-9 hours of sleep per night and establish a regular sleep routine.",]
    ],
    [
        r"(.*)stressed(.*)",
        ["Stress is a common issue. Try practicing relaxation techniques like deep breathing, meditation, or engaging in hobbies you enjoy. If stress becomes overwhelming, consider seeking professional help.",]
    ],
    [
        r"(.*)diet(.*)",
        ["Maintaining a balanced diet is important for your health. Focus on whole grains, lean proteins, fruits, and vegetables. Limit processed foods and sugary snacks.",]
    ],
    [
        r"(.*)energy levels(.*)",
        ["To improve your energy levels, ensure you're getting adequate sleep, staying hydrated, and eating a nutritious diet. Regular exercise can also help boost energy.",]
    ],
    [
        r"(.*)symptoms(.*)",
        ["Persistent symptoms should be evaluated by a healthcare professional. It's important to seek medical advice for accurate diagnosis and appropriate treatment.",]
    ],
    [
        r"(.*)thankyou(.*)",
        ["You're welcome! If you have more questions in the future, feel free to ask. Take care!",]
    ],
    [
    r"(.*)headache(.*)",
    ["If you're experiencing headaches, make sure you're hydrated, manage stress, and consider taking a break from screens.",]
],
[
    r"(.*)exercise(.*)",
    ["Regular exercise is important for overall health. Aim for at least 150 minutes of moderate-intensity exercise per week.",]
],
[
    r"(.*)weight loss(.*)",
    ["Weight loss can result from a combination of healthy eating and regular physical activity. Consult a professional for personalized advice.",]
],
[
    r"(.*)allergies(.*)",
    ["Allergies can be managed with antihistamines and avoiding triggers. If severe, consult a doctor for proper treatment.",]
],
[
    r"(.*)vaccines(.*)",
    ["Vaccines are crucial for preventing diseases. Consult your healthcare provider for recommended vaccinations.",]
],
[
    r"(.*)depression(.*)",
    ["Depression is a serious condition. Consider seeking therapy, counseling, or medication if you're struggling.",]
],
[
    r"(.*)smoking(.*)",
    ["Quitting smoking has numerous health benefits. Consider resources like nicotine replacement therapy or support groups.",]
],
[
    r"(.*)alcohol(.*)",
    ["Moderate alcohol consumption is key. Avoid excessive drinking and be aware of its impact on your health.",]
],
[
    r"(.*)skin care(.*)",
    ["Maintain healthy skin by cleansing, moisturizing, and using sunscreen. Consult a dermatologist for personalized advice.",]
],
[
    r"(.*)meditation(.*)",
    ["Meditation can reduce stress and improve mental well-being. Try apps or classes to learn meditation techniques.",]
],
[
    r"(.*)nutrition(.*)",
    ["Proper nutrition is essential for good health. Focus on a balanced diet rich in fruits, vegetables, lean proteins, and whole grains.",]
],
[
    r"(.*)hydration(.*)",
    ["Staying hydrated is important. Aim to drink at least 8 glasses of water a day to maintain proper bodily functions.",]
],
[
    r"(.*)heart health(.*)",
    ["Maintain heart health by eating a low-fat diet, exercising regularly, managing stress, and avoiding smoking.",]
],
[
    r"(.*)diabetes(.*)",
    ["If you have diabetes, monitor your blood sugar levels, take medications as prescribed, and follow a balanced diet.",]
],
[
    r"(.*)cholesterol(.*)",
    ["High cholesterol can be managed through diet and exercise. Consult a doctor if medication is needed.",]
],
[
    r"(.*)vitamins(.*)",
    ["Vitamins are essential for various bodily functions. Get a variety of nutrients from a diverse diet.",]
],
[
    r"(.*)exercise routine(.*)",
    ["Create a balanced exercise routine that includes cardiovascular, strength training, and flexibility exercises.",]
],
[
    r"(.*)back pain(.*)",
    ["For back pain, practice good posture, engage in core-strengthening exercises, and consider physical therapy.",]
],
[
    r"(.*)eye care(.*)",
    ["Protect your eyes by wearing sunglasses outdoors and taking regular breaks from screens to reduce eye strain.",]
],
[
    r"(.*)flu(.*)",
    ["To prevent the flu, consider getting a flu shot annually and practicing good hygiene, like washing your hands.",]
],
[
    r"(.*)hair care(.*)",
    ["Maintain healthy hair by using mild shampoos, avoiding excessive heat styling, and eating a balanced diet.",]
],
[
    r"(.*)stress relief(.*)",
    ["Reduce stress by practicing mindfulness, deep breathing, yoga, and engaging in activities you enjoy.",]
],
[
    r"(.*)blood pressure(.*)",
    ["Monitor your blood pressure regularly and manage it through a healthy diet, exercise, and, if needed, medication.",]
],
[
    r"(.*)pregnancy(.*)",
    ["During pregnancy, maintain regular prenatal care, eat a nutritious diet, and avoid harmful substances.",]
],
[
    r"(.*)posture(.*)",
    ["Maintain good posture to prevent back and neck pain. Sit and stand with your shoulders relaxed and back straight.",]
],
[
    r"(.*)hydration(.*)",
    ["Staying hydrated is important for overall health. Aim to drink plenty of water throughout the day.",]
],
[
    r"(.*)immune system(.*)",
    ["Boost your immune system by eating a balanced diet, exercising, getting enough sleep, and managing stress.",]
],
[
    r"(.*)caffeine(.*)",
    ["Limit caffeine intake to avoid sleep disturbances. Opt for herbal tea or decaffeinated options in the evening.",]
],
[
    r"(.*)joint pain(.*)",
    ["Manage joint pain by maintaining a healthy weight, staying active, and considering supplements like glucosamine.",]
],
[
    r"(.*)portion control(.*)",
    ["Practice portion control to avoid overeating. Use smaller plates and be mindful of serving sizes.",]
],
[
    r"(.*)protein intake(.*)",
    ["Include lean protein sources like chicken, fish, beans, and tofu in your diet for muscle health.",]
],
[
    r"(.*)gut health(.*)",
    ["Promote gut health by consuming fiber-rich foods, probiotics, and staying hydrated.",]
],
[
    r"(.*)menopause(.*)",
    ["During menopause, manage symptoms like hot flashes and mood changes with lifestyle changes and, if needed, hormone therapy.",]
],
[
    r"(.*)sun protection(.*)",
    ["Protect your skin from the sun's harmful UV rays by wearing sunscreen and protective clothing.",]
],
[
    r"(.*)aging gracefully(.*)",
    ["Practice self-care, stay active, maintain a positive mindset, and prioritize social connections for graceful aging.",]
],
[
    r"(.*)self-care(.*)",
    ["Prioritize self-care by engaging in activities that bring you joy, relaxation, and a sense of well-being.",]
],
[
    r"(.*)memory enhancement(.*)",
    ["Improve memory by staying mentally active, getting enough sleep, and practicing techniques like visualization.",]
],
[
    r"(.*)anxiety(.*)",
    ["Manage anxiety through mindfulness, deep breathing, therapy, and potentially medication under professional guidance.",]
],
[
    r"(.*)muscle building(.*)",
    ["Build muscle through strength training exercises and consuming an adequate amount of protein.",]
],
[
    r"(.*)travel health(.*)",
    ["When traveling, stay hydrated, get enough rest, and be cautious of food and water sources to prevent illness.",]
],
[
    r"(.*)portion control(.*)",
    ["Practice portion control to manage weight. Listen to your body's hunger and fullness cues.",]
],
[
    r"(.*)hormonal imbalance(.*)",
    ["If experiencing hormonal imbalance, consult a healthcare professional for evaluation and appropriate treatment options.",]
],
[
    r"(.*)mindfulness(.*)",
    ["Incorporate mindfulness into your daily routine through meditation, mindful eating, and being present in the moment.",]
],
[
    r"(.*)digestive health(.*)",
    ["Promote digestive health by consuming fiber-rich foods, staying hydrated, and managing stress.",]
],
[
    r"(.*)hair loss(.*)",
    ["Address hair loss by identifying underlying causes, using gentle hair care products, and seeking medical advice.",]
],
[
    r"(.*)stretching routine(.*)",
    ["Incorporate regular stretching into your routine to improve flexibility, prevent injuries, and reduce muscle tension.",]
],
[
    r"(.*)immune-boosting foods(.*)",
    ["Include immune-boosting foods like citrus fruits, leafy greens, and yogurt in your diet.",]
],
[
    r"(.*)mind-body connection(.*)",
    ["Cultivate a strong mind-body connection through practices like yoga, tai chi, and meditation.",]
],
[
    r"(.*)plant-based diet(.*)",
    ["Consider a plant-based diet rich in fruits, vegetables, nuts, and grains for health and sustainability.",]
],
[
    r"(.*)portion control(.*)",
    ["Control portion sizes to manage weight. Use smaller plates and focus on eating slowly and mindfully.",]
],
[
    r"(.*)work-life balance(.*)",
    ["Strive for work-life balance by setting boundaries, prioritizing self-care, and taking breaks.",]
],
[
    r"(.*)healthy snacks(.*)",
    ["Choose healthy snacks like fruits, vegetables, nuts, and yogurt to curb hunger and boost energy.",]
],
[
    r"(.*)mindful eating(.*)",
    ["Practice mindful eating by savoring each bite, eating slowly, and paying attention to hunger and fullness cues.",]
],
[
    r"(.*)coping with loss(.*)",
    ["Coping with loss can be challenging. Seek support from loved ones, therapy, or support groups.",]
],
[
    r"(.*)healthy aging(.*)",
    ["Age healthily by staying active, eating nutrient-rich foods, managing stress, and staying socially connected.",]
],
[
    r"(.*)respiratory health(.*)",
    ["Maintain respiratory health by avoiding smoking, staying active, and practicing deep breathing exercises.",]
],
[
    r"(.*)grief(.*)",
    ["Grieving is a natural process. Allow yourself to feel your emotions and seek support from others.",]
],
[
    r"(.*)hydration(.*)",
    ["Stay hydrated by drinking water throughout the day. Carry a reusable water bottle for easy access.",]
],
[
    r"(.*)bone health(.*)",
    ["Support bone health by getting enough calcium and vitamin D, and engaging in weight-bearing exercises.",]
],
[
    r"(.*)positive mindset(.*)",
    ["Cultivate a positive mindset through gratitude practice, positive self-talk, and surrounding yourself with positivity.",]
],
[
    r"(.*)fitness goals(.*)",
    ["Set realistic fitness goals and track your progress to stay motivated and achieve desired results.",]
],
[
    r"(.*)stress management(.*)",
    ["Manage stress through relaxation techniques, regular exercise, and engaging in hobbies you enjoy.",]
],
[
    r"(.*)detox diets(.*)",
    ["Be cautious of detox diets. Focus on a balanced diet and consult a healthcare professional before making drastic changes.",]
],
[
    r"(.*)workout intensity(.*)",
    ["Vary workout intensity to prevent plateaus. Incorporate both moderate and high-intensity exercises.",]
],
[
    r"(.*)balanced lifestyle(.*)",
    ["Strive for a balanced lifestyle that includes a mix of work, relaxation, socializing, and self-care.",]
],
[
    r"(.*)mind-body exercises(.*)",
    ["Mind-body exercises like yoga and Pilates promote flexibility, strength, and mental relaxation.",]
],
[
    r"(.*)portion control(.*)",
    ["Practice portion control to prevent overeating. Be mindful of portion sizes when dining out.",]
],
[
    r"(.*)stress reduction(.*)",
    ["Reduce stress through hobbies, spending time in nature, and connecting with loved ones.",]
],
[
    r"(.*)fitness accountability(.*)",
    ["Stay accountable to your fitness goals by working out with a friend or joining group classes.",]
],
[
    r"(.*)time management(.*)",
    ["Manage your time effectively by prioritizing tasks, setting deadlines, and minimizing distractions.",]
],
[
    r"(.*)happiness(.*)",
    ["Find happiness by focusing on activities that bring you joy, fostering meaningful relationships, and practicing gratitude.",]
],
[
    r"(.*)sunscreen(.*)",
    ["Apply sunscreen with at least SPF 30 to protect your skin from harmful UV rays.",]
],
[
    r"(.*)mindfulness practices(.*)",
    ["Incorporate mindfulness practices into your daily routine, such as meditation, deep breathing, and mindful eating.",]
],
[
    r"(.*)support systems(.*)",
    ["Build a strong support system by nurturing relationships with friends, family, and community.",]
],
[
    r"(.*)adaptability(.*)",
    ["Develop adaptability by embracing change, maintaining a growth mindset, and being open to new experiences.",]
],
[
    r"(.*)indoor exercises(.*)",
    ["Engage in indoor exercises like bodyweight workouts, yoga, and dance to stay active regardless of weather.",]
],
[
    r"(.*)stress relief techniques(.*)",
    ["Practice stress relief techniques such as meditation, journaling, and spending time in nature.",]
],
[
    r"(.*)meal planning(.*)",
    ["Plan meals ahead of time to make healthier choices and save time on busy days.",]
],
[
    r"(.*)mind-body connection(.*)",
    ["Cultivate a strong mind-body connection through practices like meditation, tai chi, and visualization.",]
],
[
    r"(.*)healthy relationships(.*)",
    ["Foster healthy relationships by practicing effective communication, empathy, and mutual respect.",]
],
[
    r"(.*)mindful technology use(.*)",
    ["Practice mindful technology use by setting boundaries, taking breaks, and avoiding excessive screen time.",]
],
[
    r"(.*)self-love(.*)",
    ["Practice self-love by prioritizing self-care, setting boundaries, and treating yourself with kindness.",]
],
[
    r"(.*)setting goals(.*)",
    ["Set SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound) to achieve personal and professional success.",]
],
[
    r"(.*)social connections(.*)",
    ["Maintain strong social connections by staying in touch with friends and family, even virtually.",]
],
[
    r"(.*)mindful breathing(.*)",
    ["Practice mindful breathing techniques to reduce stress and promote relaxation.",]
],
[
    r"(.*)healthy cooking(.*)",
    ["Cook meals at home using fresh ingredients to have better control over the nutritional content of your food.",]
],
[
    r"(.*)emotional well-being(.*)",
    ["Prioritize emotional well-being by expressing your feelings, seeking therapy if needed, and practicing self-compassion.",]
],
[
    r"(.*)healthy dessert options(.*)",
    ["Opt for healthier dessert options like fruit, yogurt parfaits, or dark chocolate.",]
],
[
    r"(.*)body positivity(.*)",
    ["Practice body positivity by focusing on self-acceptance and appreciating your body's capabilities.",]
],
[
    r"(.*)time for hobbies(.*)",
    ["Make time for hobbies and activities you enjoy to reduce stress and promote creativity.",]
],
[
    r"(.*)mindful walking(.*)",
    ["Practice mindful walking by paying attention to your surroundings and the sensations of each step.",]
],
[
    r"(.*)positive affirmations(.*)",
    ["Use positive affirmations to challenge negative self-talk and boost self-esteem.",]
],
[
    r"(.*)setting boundaries(.*)",
    ["Set healthy boundaries to protect your time, energy, and well-being in relationships and work.",]
],
[
    r"(.*)mindful snacking(.*)",
    ["Practice mindful snacking by savoring each bite and choosing nutritious options.",]
],
[
    r"(.*)healthy beverage choices(.*)",
    ["Choose water, herbal tea, and natural juices as healthy beverage options.",]
],
[
    r"(.*)workplace wellness(.*)",
    ["Promote workplace wellness by taking breaks, staying hydrated, and incorporating movement throughout the day.",]
],
[
    r"(.*)gratitude practice(.*)",
    ["Practice gratitude by keeping a journal of things you're thankful for each day.",]
],
[
    r"(.*)positive social media use(.*)",
    ["Use social media mindfully, following accounts that inspire you and contribute positively to your well-being.",]
],
[
    r"(.*)mindful screen time(.*)",
    ["Set limits on screen time, especially before bed, to improve sleep quality.",]
],
[
    r"(.*)laughter therapy(.*)",
    ["Engage in laughter therapy through watching comedies, attending laughter yoga classes, or spending time with funny friends.",]
],
[
    r"(.*)physical self-care(.*)",
    ["Engage in physical self-care by getting regular check-ups, taking medications as prescribed, and seeking medical attention when needed.",]
],
[
    r"(.*)healthy friendships(.*)",
    ["Nurture healthy friendships based on mutual respect, trust, and support.",]
],
[
    r"(.*)mindful technology use(.*)",
    ["Limit screen time before bed to improve sleep quality and reduce digital distractions.",]
],
[
    r"(.*)time management(.*)",
    ["Use time management techniques like the Pomodoro Technique to stay focused and productive.",]
],
 [
        r"(.*)fever(.*)",
        ["Fever can be a sign of an infection or inflammation. Monitor your temperature and stay hydrated. If it persists, consult a doctor.1. Causes:Infections: Fever is commonly associated with bacterial or viral infections such as the flu, colds, urinary tract infections, and strep throat.Inflammation: Conditions like arthritis, inflammatory bowel disease, and some autoimmune disorders can lead to fever.",]
    ],
    [
        r"(.*)cough(.*)",
        ["A persistent cough could be due to various reasons, including infections, allergies, or smoking. If it continues, seek medical advice.",]
    ],
    [
        r"(.*)fatigue(.*)",
        ["Fatigue can result from lack of sleep, stress, or underlying medical conditions. Prioritize rest, hydration, and consider a balanced diet.",]
    ],
    [
        r"(.*)pain(.*)",
        ["Pain could indicate an injury, inflammation, or other conditions. If it's severe or persistent, consult a healthcare professional for diagnosis.",]
    ],
    [
        r"(.*)shortness of breath(.*)",
        ["Shortness of breath might be due to respiratory issues or heart problems. If it's sudden or severe, seek immediate medical attention.",]
    ],
    [
        r"(.*)cold(.*)",
        ["Common cold symptoms include a runny nose, sneezing, coughing, and a sore throat. Rest, fluids, and over-the-counter cold remedies can help.",]
    ],
    [
        r"(.*)flu(.*)",
        ["Influenza (flu) symptoms include fever, body aches, fatigue, and respiratory symptoms. Rest, fluids, and antiviral medications can help.",]
    ],
    [
        r"(.*)headache(.*)",
        ["Headaches can result from various causes, including tension, dehydration, or migraines. Identify triggers and manage stress.",]
    ],
    [
        r"(.*)fever(.*)",
        ["Fever is a common symptom of various infections and illnesses. Rest, fluids, and fever-reducing medications can help manage fever.",]
    ],
    [
        r"(.*)cough(.*)",
        ["Coughing can be caused by colds, flu, allergies, or respiratory infections. Stay hydrated and consider cough medicines if needed.",]
    ],
    [
        r"(.*)stomachache(.*)",
        ["Stomachaches may be due to indigestion, food poisoning, or gastrointestinal issues. Avoid spicy foods and stay hydrated.",]
    ],
    [
        r"(.*)fatigue(.*)",
        ["Fatigue can result from lack of sleep, stress, or underlying health conditions. Get adequate rest and consider lifestyle changes.",]
    ],
    [
        r"(.*)rash(.*)",
        ["Rashes can be caused by allergies, skin irritants, or infections. Keep the affected area clean and consider topical treatments.",]
    ],
    [
        r"(.*)sore throat(.*)",
        ["Sore throats can be caused by viral infections or strep throat. Rest, warm liquids, and throat lozenges can provide relief.",]
    ],
    [
        r"(.*)diarrhea(.*)",
        ["Diarrhea may be due to infections, food intolerances, or gastrointestinal issues. Stay hydrated and consider bland foods.",]
    ],
    [
        r"(.*)nausea(.*)",
        ["Nausea can result from various factors including motion sickness, food poisoning, or infections. Stay hydrated and consider ginger remedies.",]
    ],
    [
        r"(.*)allergies(.*)",
        ["Allergies can cause symptoms like sneezing, itching, and congestion. Avoid triggers and consider antihistamines if recommended by a doctor.",]
    ],
    [
        r"(.*)asthma(.*)",
        ["Asthma is a chronic respiratory condition that can cause wheezing, shortness of breath, and chest tightness. Inhalers and medication can help manage symptoms.",]
    ],
    [
        r"(.*)diabetes(.*)",
        ["Diabetes is a metabolic condition that affects blood sugar levels. Proper diet, exercise, and medication are important for managing diabetes.",]
    ],
    [
        r"(.*)hypertension(.*)",
        ["Hypertension, or high blood pressure, can increase the risk of heart disease. Lifestyle changes and medication can help control blood pressure.",]
    ],
    [
        r"(.*)cholesterol(.*)",
        ["High cholesterol levels can increase the risk of heart disease. A healthy diet, exercise, and medication can help manage cholesterol levels.",]
    ],
    [
        r"(.*)anxiety(.*)",
        ["Anxiety is a common mental health condition. Practice relaxation techniques, seek support, and consider therapy if anxiety is affecting daily life.",]
    ],
    [
        r"(.*)depression(.*)",
        ["Depression is a mood disorder that can impact daily functioning. Therapy, medication, and lifestyle changes can help manage depressive symptoms.",]
    ],
    [
        r"(.*)insomnia(.*)",
        ["Insomnia is a sleep disorder characterized by difficulty falling asleep or staying asleep. Create a bedtime routine and consider relaxation techniques.",]
    ],
    [
        r"(.*)back pain(.*)",
        ["Back pain can result from poor posture, muscle strain, or spinal issues. Practice good posture, gentle stretches, and consider pain relief methods.",]
    ],
    [
        r"(.*)joint pain(.*)",
        ["Joint pain can be caused by arthritis, injury, or inflammation. Rest, gentle exercises, and anti-inflammatory medications may help alleviate discomfort.",]
    ],
    [
        r"(.*)skin acne(.*)",
        ["Acne is a common skin condition that can result from hormonal changes, genetics, or poor skincare. Maintain a clean skincare routine and consider treatment options.",]
    ],
    [
        r"(.*)hair loss(.*)",
        ["Hair loss can have various causes including genetics, stress, and medical conditions. Consult a dermatologist for personalized advice and treatment options.",]
    ],
    [
        r"(.*)digestive problems(.*)",
        ["Digestive issues like indigestion, bloating, and constipation can result from dietary choices or underlying conditions. Maintain a balanced diet and stay hydrated.",]
    ],
    [
        r"(.*)heartburn(.*)",
        ["Heartburn can be triggered by certain foods, alcohol, or acid reflux. Avoid trigger foods, eat smaller meals, and consider over-the-counter antacids.",]
    ],
    [
        r"(.*)irritable bowel syndrome(.*)",
        ["Irritable bowel syndrome (IBS) can cause abdominal discomfort, bloating, and changes in bowel habits. Manage symptoms through diet, stress reduction, and medication.",]
    ],
    [
        r"(.*)menstrual cramps(.*)",
        ["Menstrual cramps are common during menstruation. Applying heat, staying hydrated, and over-the-counter pain relievers can provide relief.",]
    ],
    [
        r"(.*)pregnancy(.*)",
        ["Pregnancy comes with various changes and challenges. Prenatal care, a balanced diet, and regular exercise are important for a healthy pregnancy.",]
    ],
    [
        r"(.*)menopause(.*)",
        ["Menopause brings hormonal changes that can result in hot flashes, mood swings, and other symptoms. Hormone therapy, lifestyle changes, and self-care can help manage symptoms.",]
    ],
    [
        r"(.*)osteoporosis(.*)",
        ["Osteoporosis is a condition characterized by weakened bones. Calcium-rich diet, weight-bearing exercises, and medications can help prevent and manage osteoporosis.",]
    ],
    [
        r"(.*)urinary tract infection(.*)",
        ["Urinary tract infections (UTIs) can cause discomfort during urination and frequent urination. Drink plenty of water and consult a doctor for antibiotics if needed.",]
    ],
    [
        r"(.*)allergic reactions(.*)",
        ["Allergic reactions can range from mild to severe. Avoid allergens, carry an epinephrine auto-injector if necessary, and seek medical help for severe reactions.",]
    ],
    [
        r"(.*)asthma exacerbation(.*)",
        ["Asthma exacerbation is a sudden worsening of asthma symptoms. Use rescue inhalers as prescribed, avoid triggers, and seek medical help if symptoms worsen.",]
    ],
    [
        r"(.*)heart attack(.*)",
        ["A heart attack occurs when blood flow to the heart muscle is blocked. Recognize symptoms like chest pain, shortness of breath, and seek emergency medical care.",]
    ],
    [
        r"(.*)stroke(.*)",
        ["A stroke occurs when blood flow to the brain is disrupted. Recognize symptoms like facial drooping, arm weakness, and speech difficulties. Seek immediate medical attention.",]
    ],
    [
        r"(.*)diarrhea in children(.*)",
        ["Diarrhea in children can result from infections or dietary changes. Maintain hydration with fluids and oral rehydration solutions. Consult a doctor if symptoms persist.",]
    ],
    [
        r"(.*)childhood vaccinations(.*)",
        ["Childhood vaccinations are important for preventing various diseases. Follow recommended vaccination schedules to ensure your child's health and well-being.",]
    ],
    [
        r"(.*)childhood obesity(.*)",
        ["Childhood obesity can lead to various health issues. Encourage a balanced diet, regular physical activity, and limit screen time to promote a healthy lifestyle for children.",]
    ],
    [
        r"(.*)elderly fall prevention(.*)",
        ["Fall prevention is crucial for the elderly. Keep living spaces clear of hazards, use assistive devices if needed, and engage in balance exercises to reduce the risk of falls.",]
    ],
    #intro pairs
    [
        r"my name is (.*)",
        ["Hello! Nice to meet you. How can I assist you with your health-related questions?",]
    ],
    [
        r"i am ",
        ["Hi there! How can I be of help with your health and wellness inquiries?",]
    ],
    [
        r"(.*)hello(.*)",
        ["Hello! How can I assist you with your health and wellness needs?",]
    ],
    [
        r"(.*)hey(.*)",
        ["Hey there! How can I help you today with your health-related queries?",]
    ],
    [
        r"(.*)hai(.*)",
        ["Hi! Welcome. How can I support you with your health-related questions?",]
    ],
    [
        r"(.*)hi(.*)",
        ["Hi! Welcome. How can I support you with your health-related questions?",]
    ],
    [
        r"good day",
        ["Good day! How can I be of service to you regarding health and wellness?",]
    ],
    [
        r"howdy",
        ["Howdy! How can I assist you today with your health inquiries?",]
    ],
    [
        r"greetings",
        ["Greetings! How can I help you with your health and wellness concerns?",]
    ],
    [
        r"nice to meet you",
        ["Nice to meet you too! How can I assist you with your health-related questions?",]
    ],
    [
        r"pleased to meet you",
        ["Pleased to meet you as well! How can I support you in matters of health and wellness?",]
    ],
    [
        r"hello bot",
        ["Hello! How can I be of service to you regarding health and wellness?",]
    ],
    [
        r"hi bot",
        ["Hi! Welcome. How can I assist you today with your health-related queries?",]
    ],
    [
        r"hey bot",
        ["Hey there! How can I help you today with your health and wellness needs?",]
    ],
    [
        r"how are you",
        ["I'm just a computer program, but I'm here and ready to help you with any health-related questions you have.",]
    ],
    [
        r"tell me about yourself",
        ["I'm a health assistant bot here to provide information and answer your health-related queries. How can I assist you?",]
    ],
    [
        r"who are you",
        ["I'm a health assistant bot designed to provide information and answer your health-related questions. How can I help you today?",]
    ],
    [
        r"what can you do",
        ["I'm here to help answer your health-related questions and provide information on various health topics. Feel free to ask me anything.",]
    ],
    [
        r"nice to see you",
        ["Nice to interact with you as well! How can I support you with your health and wellness inquiries?",]
    ],
    [
        r"good to meet you",
        ["Good to meet you too! How can I assist you with your health-related questions?",]
    ],
    [
        r"how can you help me",
        ["I'm here to provide information and answer your health-related questions. Feel free to ask me about various health topics.",]
    ],
    [
        r"what's your purpose",
        ["My purpose is to assist you with your health and wellness inquiries. Ask me anything related to health.",]
    ],
    [
        r"what do you know about health",
        ["I have information on a wide range of health topics, from common ailments to general wellness advice. How can I assist you?",]
    ],
    [
        r"how does this work",
        ["You can ask me health-related questions, and I'll do my best to provide accurate information and guidance.",]
    ],
    [
        r"can you give health advice",
        ["While I can provide general information, it's always best to consult a healthcare professional for personalized health advice.",]
    ],
    [
        r"where do you get your information",
        ["I've been trained on a wide range of health-related data sources to provide accurate information and answers.",]
    ],
    [
        r"what topics can you cover",
        ["I can cover topics such as nutrition, exercise, common illnesses, mental health, and more. Feel free to ask!",]
    ],
    [
        r"how reliable are your responses",
        ["I strive to provide accurate and reliable information, but always verify with trusted sources or professionals for critical decisions.",]
    ],
    [
        r"do you have medical knowledge",
        ["I have a database of health-related information, but I'm not a substitute for professional medical advice. Consult a doctor for medical concerns.",]
    ],
    [
        r"can you help with a specific condition",
        ["I can provide general information about various conditions, but it's recommended to consult a doctor for accurate diagnosis and advice.",]
    ],
    [
        r"tell me about your features",
        ["I can answer health-related questions, provide wellness tips, and offer guidance. How can I assist you today?",]
    ],
    [
        r"are you a doctor",
        ["No, I'm not a doctor. I'm a chatbot designed to provide health information and answer your questions.",]
    ],
    [
        r"how do I use this chat",
        ["Simply type your health-related question or topic, and I'll do my best to provide you with relevant information.",]
    ],
    [
        r"can you help with mental health",
        ["I can provide general advice on mental health, but for serious concerns, consider speaking to a mental health professional.",]
    ],
    [
        r"what languages do you understand",
        ["I primarily understand and communicate in English. Feel free to ask your questions in English.",]
    ],
    [
        r"tell me a joke",
        ["Sure, here's a joke: Why did the scarecrow win an award? Because he was outstanding in his field!",]
    ],
    [
        r"can you recommend a healthy diet",
        ["A balanced diet includes fruits, vegetables, whole grains, lean proteins, and healthy fats. Consult a nutritionist for personalized plans.",]
    ],
    [
        r"how do I stay fit",
        ["Regular exercise, staying active, and maintaining a healthy diet are key to staying fit. Consider talking to a fitness expert for guidance.",]
    ],
    [
        r"how can I improve my sleep",
        ["Creating a bedtime routine, keeping a consistent sleep schedule, and creating a comfortable sleep environment can improve sleep quality.",]
    ],
    [
        r"what's the best way to manage stress",
        ["Managing stress involves relaxation techniques, exercise, mindfulness, and seeking support from friends, family, or professionals.",]
    ],
    #endingpairs
    [
        r"(.*)thank you(.*)",
        ["You're welcome! If you have more questions in the future, feel free to ask. Take care!",]
    ],
    [
        r"(.*)thanks for your help(.*)",
        ["You're welcome! If you need assistance again, don't hesitate to reach out. Have a great day!",]
    ],
    [
        r"(.*)goodbye(.*)",
        ["Goodbye! If you ever need information or advice, feel free to come back and chat with me.",]
    ],
    [
        r"(.*)bye(.*)",
        ["Bye! If you have more questions in the future, don't hesitate to ask. Stay healthy!",]
    ],
    [
        r"(.*)have a great day(.*)",
        ["Thank you! Wishing you a wonderful day ahead. Feel free to return if you need any health-related information.",]
    ],
    [
        r"(.*)take care(.*)",
        ["You too! Remember to prioritize your health and well-being. If you have more questions, don't hesitate to ask.",]
    ],
    [
        r"see you later",
        ["See you later! If you ever need assistance or health information, feel free to come back and chat.",]
    ],
    [
        r"farewell",
        ["Farewell! If you have more health-related inquiries in the future, feel free to reach out.",]
    ],
    [
        r"until next time",
        ["Until next time! Stay well and take care of yourself. If you have more questions, I'll be here.",]
    ],
    [
        r"have a nice day",
        ["Thank you! Wishing you a pleasant day ahead. If you need more information, feel free to return.",]
    ],
    [
        r"thanks, goodbye",
        ["You're welcome! If you ever need assistance or have health-related questions, don't hesitate to ask. Goodbye!",]
    ],
    [
        r"good chatting with you",
        ["Likewise! If you have more questions or topics to discuss, feel free to reach out again. Take care!",]
    ],
    [
        r"until we meet again",
        ["Until then, stay healthy and take care. If you have more inquiries, remember you can always chat with me.",]
    ],
    [
        r"appreciate your help",
        ["I'm glad I could assist you. If you need help or information in the future, don't hesitate to ask. Farewell!",]
    ],
    [
        r"have a wonderful day",
        ["Thank you! Wishing you a wonderful and healthy day. If you have more questions, feel free to come back.",]
    ],
    [
        r"take care of yourself",
        ["You too! Remember to prioritize your health and well-being. If you have more inquiries, feel free to ask.",]
    ],
    [
        r"(.*)thank you, goodbye(.*)",
        ["You're welcome! If you ever need health-related information or advice, don't hesitate to chat with me again. Goodbye!",]
    ],
    [
        r"it was nice chatting",
        ["Likewise! If you have more topics to discuss or questions to ask, don't hesitate to reach out again. Take care!",]
    ],
    [
        r"(.*)see you soon(.*)",
        ["See you soon! Remember, I'm here to help with your health-related queries whenever you need assistance.",]
    ],
    [
        r"(.*)goodbye, stay well(.*)",
        ["Goodbye! Stay well and take care of yourself. If you have more questions or concerns, feel free to chat.",]
    ],
    [
        r"(.*)have a great weekend(.*)",
        ["Thank you! Wishing you a fantastic weekend ahead. If you need more health information, feel free to return.",]
    ],
    [
        r"thank you for your time",
        ["You're welcome! If you have more questions or need assistance in the future, don't hesitate to reach out. Goodbye!",]
    ],
    [
        r"(.*)goodbye, take care(.*)",
        ["Goodbye! Take care of yourself and stay well. If you ever need health advice, feel free to chat with me again.",]
    ],
    [
        r"(.*)it's been helpful(.*)",
        ["I'm glad I could help. If you ever need more information or advice, remember you can always chat with me. Farewell!",]
    ],
    [
        r"(.*)see you next time(.*)",
        ["See you next time! If you have more inquiries or health-related topics to discuss, don't hesitate to reach out.",]
    ],
    [
        r"bye for now",
        ["Goodbye for now! If you need health information or have questions in the future, feel free to return.",]
    ],
    [
        r"have a pleasant day",
        ["Thank you! Wishing you a pleasant and healthy day. If you have more questions, feel free to come back.",]
    ],
    [
        r"thanks for the advice",
        ["You're welcome! If you need further advice or information on health topics, don't hesitate to ask. Take care!",]
    ],
    [
        r"farewell, stay healthy",
        ["Farewell! Remember to prioritize your health and well-being. If you have more questions, feel free to chat.",]
    ],
    [
        r"until we chat again",
        ["Until our next chat! If you have more health-related queries or concerns, don't hesitate to reach out.",]
    ],
    [
        r"goodbye, be well",
        ["Goodbye! Be well and take care of yourself. If you need more information or assistance, feel free to return.",]
    ],
    [
        r"take care, goodbye",
        ["You too! Take care and stay healthy. If you have more questions or topics to discuss, I'm here to help.",]
    ],
    [
        r"thanks for the chat",
        ["You're welcome! If you need more information or advice on health matters, don't hesitate to chat with me again.",]
    ],
    [
        r"see you on the next chat",
        ["Looking forward to our next chat! If you need assistance or have inquiries, remember I'm here to help.",]
    ],
    [
        r"so long, stay well",
        ["So long! Take care of yourself and your health. If you have more questions, feel free to reach out.",]
    ],
    [
        r"goodbye, stay safe",
        ["Goodbye! Stay safe and healthy. If you need more health information or advice, don't hesitate to ask.",]
    ],
    [
        r"thank you, stay well",
        ["You're welcome! Wishing you wellness and good health. If you have more questions, feel free to come back.",]
    ],
    [
        r"it's been informative",
        ["I'm glad I could provide information. If you need more insights or health advice, remember I'm here to help.",]
    ],
    [
        r"see you again soon",
        ["Looking forward to our next conversation! If you need health-related information, feel free to chat with me again.",]
    ],
    [
        r"goodbye, take good care",
        ["Goodbye! Take good care of yourself and your health. If you have more inquiries, don't hesitate to ask.",]
    ], 
    #negative pairs
    [
        r"(.*)frustrating(.*)",
        ["I understand it can be frustrating. Please let me know if you have any health questions or topics you'd like to discuss.",]
    ],
    [
        r"(.*)not satisfied(.*)",
        ["I'm sorry to hear that. If you need health-related information or advice, feel free to ask, and I'll do my best to assist you.",]
    ],
    [
        r"(.*)useless(.*)",
        ["I'm sorry if my response felt that way. If you have health concerns or queries, please let me know so I can provide better assistance.",]
    ],
    [
        r"(.*)confused(.*)",
        ["I apologize if my response was confusing. Feel free to ask any health-related questions you have, and I'll provide clearer information.",]
    ],
    [
        r"(.*)not helpful(.*)",
        ["I'm sorry my response didn't help. Let me know what health information you're seeking, and I'll do my best to provide relevant answers.",]
    ],
    [
        r"(.*)expected more(.*)",
        ["I apologize if my response fell short of your expectations. If you need health advice or information, please specify the topic.",]
    ],
    [
        r"(.*)unsatisfactory(.*)",
        ["I'm sorry if you found my response unsatisfactory. Please share your health-related concerns or questions so I can assist you better.",]
    ],
    [
        r"(.*)disappointed(.*)",
        ["I'm sorry to hear that. If you have health inquiries or topics you'd like to discuss, please let me know for better assistance.",]
    ],
    [
        r"(.*)not what I needed(.*)",
        ["I apologize if my response didn't meet your needs. If you have specific health concerns, feel free to ask, and I'll try to provide relevant information.",]
    ],
    [
        r"(.*)unhelpful(.*)",
        ["I'm sorry if my response was unhelpful. If you have health-related questions, let me know so I can provide more useful information.",]
    ],
    [
        r"(.*)dissatisfied(.*)",
        ["I'm sorry if my previous response didn't meet your expectations. If you need health advice or guidance, please let me know.",]
    ],
    [
        r"(.*)not satisfied(.*)",
        ["I'm sorry to hear that. If you have health-related questions or concerns, please share them, and I'll provide better assistance.",]
    ],
    [
        r"(.*)waste(.*)",
        ["I apologize if you feel that way. If you have any health concerns or questions, please share them, and I'll do my best to assist you.",]
    ],
    [
        r"(.*)didn't help(.*)",
        ["I'm sorry if my response didn't provide the information you needed. Feel free to ask any health-related questions you have.",]
    ],
    [
        r"(.*)useless(.*)",
        ["I'm here to help with health-related queries. If you have any questions or topics you'd like to discuss, please let me know.",]
    ],
    [
        r"(.*)confusing(.*)",
        ["I apologize if my previous response was confusing. If you need health advice or information, feel free to ask for clarification.",]
    ],
    [
        r"(.*)no(.*)",
        ["I'm sorry if my response didn't meet your expectations. Let me know what health information you're looking for.",]
    ],
    [
        r"(.*)unsatisfactory(.*)",
        ["I apologize if my answer didn't satisfy you. If you have health concerns or questions, please share them for better assistance.",]
    ],
    [
        r"(.*)useless(.*)",
        ["I'm here to help with health-related inquiries. If you have any questions or topics you'd like to discuss, please let me know.",]
    ],
    [
        r"(.*)disappointed(.*)",
        ["I'm sorry to hear that. If you need health advice or information, please let me know how I can assist you better.",]
    ],
    [
        r"(.*)not what I wanted(.*)",
        ["I apologize if my response didn't provide the information you were looking for. Feel free to ask any specific health-related questions.",]
    ],
    [
        r"(.*)unhelpful(.*)",
        ["I'm sorry if my response wasn't helpful. If you have health concerns or inquiries, please share them for more relevant information.",]
    ],
    [
        r"(.*)useless(.*)",
        ["I apologize if my previous response felt useless. If you need health advice or guidance, please let me know.",]
    ],
    [
        r"(.*)not satisfied(.*)",
        ["I'm sorry if I haven't met your expectations. If you have health-related questions or topics you'd like to discuss, please share them.",]
    ],
    [
        r"(.*)bad(.*)",
        ["I'm here to assist with health-related inquiries. If you have questions or concerns, please let me know how I can help.",]
    ],
    [
        r"(.*)bad response(.*)",
        ["I apologize if my response didn't meet your expectations. If you have health concerns or questions, please share them.",]
    ],
    [
        r"(.*)not what I needed(.*)",
        ["I'm sorry if my previous response didn't address your needs. If you have specific health inquiries, feel free to ask.",]
    ],
    [
        r"(.*)disappointed in this bot(.*)",
        ["I'm here to help with health-related queries. If you have questions or topics you'd like to discuss, please let me know.",]
    ],
    [
        r"(.*)not helpful at all(.*)",
        ["I apologize if my response wasn't helpful. If you have health concerns or questions, please share them for better assistance.",]
    ],
    [
        r"(.*)expected more from bot(.*)",
        ["I'm here to provide health-related information and advice. If you need assistance or have questions, feel free to ask.",]
    ],
    [
        r"(.*)terrible(.*)",
        ["I'm sorry if I've fallen short of your expectations. If you have health-related inquiries, please let me know how I can assist you better.",]
    ],
    [
        r"(.*)terrible response(.*)",
        ["I apologize if my response didn't meet your needs. If you have health concerns or questions, please share them for better assistance.",]
    ],
]
chatbot = Chat(pairs, reflections)

# Update the chatbot_response function to return text and audio as bytes
def chatbot_response(user_message):
    for pattern, responses in pairs:
        match = re.match(pattern, user_message, re.IGNORECASE)
        if match:
            text_response = random.choice(responses)
            tts = gTTS(text_response)
            audio_filename = "response.mp3"
            tts.save(audio_filename)  # Save the TTS audio to a file
            with open(audio_filename, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            return text_response, audio_bytes  # Return as separate values
    return (
        "I'm sorry, but I didn't quite understand that. Could you please rephrase or ask another question?",
        None
    )

@app.route('/backend/get_response', methods=['POST'])
def get_response():
    
    user_message = request.json['message']
    text_response, audio_bytes = chatbot_response(user_message)

    if audio_bytes:
     audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
     return jsonify({'response': text_response, 'audio': audio_base64})
    else:
        return jsonify({'response': text_response, 'audio': None})

if __name__ == '__main__':
    app.run(debug=True)

