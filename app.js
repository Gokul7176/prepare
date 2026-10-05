/**
 * FLYORA INDIA – SMART FLIGHT BOOKING SYSTEM
 * Core Application Engine & Interactive State Management
 * Tailored for Indian Skies & Indian Rupee (INR - ₹) Transactions
 */

// ==========================================
// 1. GLOBAL STATE & DATA REGISTRY
// ==========================================
const AppState = {
  theme: localStorage.getItem('flyora_theme') || 'dark',
  currency: {
    code: 'INR',
    symbol: '₹',
    rate: 1.0,
    flag: '🇮🇳'
  },
  search: {
    tripType: 'one-way',
    fareType: 'regular',
    origin: { code: 'DEL', city: 'New Delhi', country: 'India', name: 'Indira Gandhi International Airport' },
    destination: { code: 'BOM', city: 'Mumbai', country: 'India', name: 'Chhatrapati Shivaji Maharaj Intl' },
    departDate: getFutureDate(7),
    returnDate: getFutureDate(14),
    passengers: { adult: 1, child: 0, infant: 0 },
    cabinClass: 'economy'
  },
  filters: {
    maxPrice: 30000,
    stops: ['0', '1', '2'],
    airlines: [],
    timeSlot: 'all',
    wifi: false,
    power: false,
    meal: false
  },
  sortBy: 'cheapest',
  currentFlights: [],
  selectedFlight: null,
  booking: {
    step: 1,
    paxDetails: {
      firstName: 'Aarav',
      lastName: 'Sharma',
      email: 'aarav.sharma@example.com',
      phone: '+91 98765 43210',
      nationality: 'IN',
      dob: '1996-08-15',
      passport: 'XXXX-XXXX-4892'
    },
    selectedSeat: '14B',
    selectedSeatPrice: 0,
    addons: {
      baggage: false,
      meal: false,
      priority: false,
      insurance: true,
      carbon: false
    },
    payment: {
      method: 'upi'
    }
  },
  savedTrips: JSON.parse(localStorage.getItem('flyora_trips') || '[]')
};

// Helper: Future Date String YYYY-MM-DD
function getFutureDate(daysAhead) {
  const d = new Date();
  d.setDate(d.getDate() + daysAhead);
  return d.toISOString().split('T')[0];
}

// Comprehensive Database of All Commercial & Regional Indian Airports
const AIRPORTS = [
  // --- METROPOLITAN & MAJOR INTERNATIONAL HUBS ---
  { code: 'DEL', city: 'New Delhi', state: 'Delhi (NCR)', country: 'India', name: 'Indira Gandhi International Airport (T3/T2/T1)', digiYatra: true, popular: true },
  { code: 'BOM', city: 'Mumbai', state: 'Maharashtra', country: 'India', name: 'Chhatrapati Shivaji Maharaj International Airport (CSMIA T2/T1)', digiYatra: true, popular: true },
  { code: 'BLR', city: 'Bengaluru', state: 'Karnataka', country: 'India', name: 'Kempegowda International Airport (T2 Garden Terminal/T1)', digiYatra: true, popular: true },
  { code: 'MAA', city: 'Chennai', state: 'Tamil Nadu', country: 'India', name: 'Chennai International Airport (T1 Domestic / T2 & T4 Intl)', digiYatra: true, popular: true },
  { code: 'CCU', city: 'Kolkata', state: 'West Bengal', country: 'India', name: 'Netaji Subhash Chandra Bose International Airport', digiYatra: true, popular: true },
  { code: 'HYD', city: 'Hyderabad', state: 'Telangana', country: 'India', name: 'Rajiv Gandhi International Airport (RGIA Shamshabad)', digiYatra: true, popular: true },
  { code: 'AMD', city: 'Ahmedabad', state: 'Gujarat', country: 'India', name: 'Sardar Vallabhbhai Patel International Airport (T1/T2)', digiYatra: true, popular: true },
  { code: 'PNQ', city: 'Pune', state: 'Maharashtra', country: 'India', name: 'Pune International Airport (New Integrated Terminal)', digiYatra: true, popular: true },

  // --- GOA ---
  { code: 'GOI', city: 'Goa (Dabolim)', state: 'Goa', country: 'India', name: 'Dabolim International Airport (South Goa)', digiYatra: true, popular: true },
  { code: 'GOX', city: 'Goa (Mopa)', state: 'Goa', country: 'India', name: 'Manohar International Airport (Mopa, North Goa)', digiYatra: true, popular: true },

  // --- NORTHERN INDIA (J&K, LADAKH, HP, PUNJAB, HARYANA, UTs) ---
  { code: 'SXR', city: 'Srinagar', state: 'Jammu & Kashmir', country: 'India', name: 'Sheikh ul-Alam International Airport', digiYatra: true, popular: true },
  { code: 'IXJ', city: 'Jammu', state: 'Jammu & Kashmir', country: 'India', name: 'Jammu Civil Airport (Satwari)', digiYatra: false },
  { code: 'IXL', city: 'Leh Ladakh', state: 'Ladakh', country: 'India', name: 'Kushok Bakula Rimpochee Airport (High Altitude)', digiYatra: false, popular: true },
  { code: 'KRG', city: 'Kargil', state: 'Ladakh', country: 'India', name: 'Kargil Civil Airport', digiYatra: false },
  { code: 'ATQ', city: 'Amritsar', state: 'Punjab', country: 'India', name: 'Sri Guru Ram Dass Jee International Airport', digiYatra: false, popular: true },
  { code: 'IXC', city: 'Chandigarh', state: 'Punjab / Haryana', country: 'India', name: 'Shaheed Bhagat Singh International Airport (Mohali)', digiYatra: true },
  { code: 'AIP', city: 'Adampur (Jalandhar)', state: 'Punjab', country: 'India', name: 'Adampur Airport (Civil Enclave)', digiYatra: false },
  { code: 'BTI', city: 'Bathinda', state: 'Punjab', country: 'India', name: 'Bathinda Airport (Virpal)', digiYatra: false },
  { code: 'LUH', city: 'Ludhiana', state: 'Punjab', country: 'India', name: 'Sahnewal Airport', digiYatra: false },
  { code: 'HSS', city: 'Hisar', state: 'Haryana', country: 'India', name: 'Maharaja Agrasen Airport', digiYatra: false },
  { code: 'DHM', city: 'Dharamshala (Kangra)', state: 'Himachal Pradesh', country: 'India', name: 'Gaggal Airport (Kangra Airport)', digiYatra: false },
  { code: 'KUU', city: 'Kullu (Manali)', state: 'Himachal Pradesh', country: 'India', name: 'Kullu–Manali Airport (Bhuntar)', digiYatra: false },
  { code: 'SLV', city: 'Shimla', state: 'Himachal Pradesh', country: 'India', name: 'Shimla Airport (Jubbarhatti)', digiYatra: false },

  // --- UTTAR PRADESH & UTTARAKHAND ---
  { code: 'LKO', city: 'Lucknow', state: 'Uttar Pradesh', country: 'India', name: 'Chaudhary Charan Singh International Airport (T3/T2)', digiYatra: true, popular: true },
  { code: 'VNS', city: 'Varanasi', state: 'Uttar Pradesh', country: 'India', name: 'Lal Bahadur Shastri International Airport (Babatpur)', digiYatra: true, popular: true },
  { code: 'AYJ', city: 'Ayodhya', state: 'Uttar Pradesh', country: 'India', name: 'Maharishi Valmiki International Airport (Dham)', digiYatra: true, popular: true },
  { code: 'IXD', city: 'Prayagraj (Allahabad)', state: 'Uttar Pradesh', country: 'India', name: 'Prayagraj Civil Airport (Bamrauli)', digiYatra: false },
  { code: 'KNU', city: 'Kanpur', state: 'Uttar Pradesh', country: 'India', name: 'Kanpur Civil Aerodrome (Chakeri New Terminal)', digiYatra: false },
  { code: 'AGR', city: 'Agra', state: 'Uttar Pradesh', country: 'India', name: 'Agra Civil Airport (Kheria Air Force Station)', digiYatra: false },
  { code: 'BEK', city: 'Bareilly', state: 'Uttar Pradesh', country: 'India', name: 'Bareilly Airport (Civil Enclave Trishul)', digiYatra: false },
  { code: 'GOP', city: 'Gorakhpur', state: 'Uttar Pradesh', country: 'India', name: 'Mahayogi Gorakhnath Airport', digiYatra: false },
  { code: 'AHH', city: 'Aligarh', state: 'Uttar Pradesh', country: 'India', name: 'Aligarh Airport', digiYatra: false },
  { code: 'MZS', city: 'Moradabad', state: 'Uttar Pradesh', country: 'India', name: 'Moradabad Airport', digiYatra: false },
  { code: 'HDO', city: 'Hindon (Ghaziabad / NCR)', state: 'Uttar Pradesh', country: 'India', name: 'Hindon Civil Enclave Air Force Station', digiYatra: false },
  { code: 'DED', city: 'Dehradun (Rishikesh)', state: 'Uttarakhand', country: 'India', name: 'Jolly Grant Airport (Dehradun Intl)', digiYatra: true },
  { code: 'PGH', city: 'Pantnagar (Nainital)', state: 'Uttarakhand', country: 'India', name: 'Pantnagar Airport (Jim Corbett)', digiYatra: false },
  { code: 'NNS', city: 'Pithoragarh', state: 'Uttarakhand', country: 'India', name: 'Naini Saini Airport', digiYatra: false },

  // --- RAJASTHAN ---
  { code: 'JAI', city: 'Jaipur', state: 'Rajasthan', country: 'India', name: 'Jaipur International Airport (T2 Sanganer)', digiYatra: true, popular: true },
  { code: 'UDR', city: 'Udaipur', state: 'Rajasthan', country: 'India', name: 'Maharana Pratap Airport (Dabok)', digiYatra: false, popular: true },
  { code: 'JDH', city: 'Jodhpur', state: 'Rajasthan', country: 'India', name: 'Jodhpur Civil Airport', digiYatra: false },
  { code: 'JSA', city: 'Jaisalmer', state: 'Rajasthan', country: 'India', name: 'Jaisalmer Civil Airport', digiYatra: false },
  { code: 'BKN', city: 'Bikaner', state: 'Rajasthan', country: 'India', name: 'Nal Airport (Bikaner Civil Enclave)', digiYatra: false },
  { code: 'KQH', city: 'Kishangarh (Ajmer/Pushkar)', state: 'Rajasthan', country: 'India', name: 'Kishangarh Airport', digiYatra: false },

  // --- GUJARAT & DIU ---
  { code: 'STV', city: 'Surat', state: 'Gujarat', country: 'India', name: 'Surat International Airport (Diamond City Hub)', digiYatra: true },
  { code: 'BDQ', city: 'Vadodara', state: 'Gujarat', country: 'India', name: 'Vadodara Airport (Civil Aerodrome Harni)', digiYatra: false },
  { code: 'RAJ', city: 'Rajkot', state: 'Gujarat', country: 'India', name: 'Rajkot International Airport (Hirasar Greenfield)', digiYatra: false },
  { code: 'BHU', city: 'Bhavnagar', state: 'Gujarat', country: 'India', name: 'Bhavnagar Airport', digiYatra: false },
  { code: 'BHJ', city: 'Bhuj (Kutch)', state: 'Gujarat', country: 'India', name: 'Bhuj Airport (Rudra Mata Air Force Station)', digiYatra: false },
  { code: 'JGA', city: 'Jamnagar', state: 'Gujarat', country: 'India', name: 'Jamnagar Airport (Govardhanpur)', digiYatra: false },
  { code: 'PBD', city: 'Porbandar', state: 'Gujarat', country: 'India', name: 'Porbandar Airport', digiYatra: false },
  { code: 'KSD', city: 'Keshod (Gir Forest)', state: 'Gujarat', country: 'India', name: 'Keshod Airport', digiYatra: false },
  { code: 'DIU', city: 'Diu', state: 'Daman & Diu', country: 'India', name: 'Diu Civil Aerodrome', digiYatra: false },
  { code: 'IXM', city: 'Mundra', state: 'Gujarat', country: 'India', name: 'Mundra Commercial Airport', digiYatra: false },

  // --- MAHARASHTRA ---
  { code: 'NAG', city: 'Nagpur', state: 'Maharashtra', country: 'India', name: 'Dr. Babasaheb Ambedkar International Airport', digiYatra: false },
  { code: 'SAG', city: 'Shirdi', state: 'Maharashtra', country: 'India', name: 'Shirdi International Airport (Kakadi)', digiYatra: false, popular: true },
  { code: 'IXU', city: 'Chhatrapati Sambhajinagar (Aurangabad)', state: 'Maharashtra', country: 'India', name: 'Chhatrapati Sambhajinagar Airport (Ellora/Ajanta)', digiYatra: false },
  { code: 'KLH', city: 'Kolhapur', state: 'Maharashtra', country: 'India', name: 'Chhatrapati Rajaram Maharaj Airport', digiYatra: false },
  { code: 'NDC', city: 'Nanded', state: 'Maharashtra', country: 'India', name: 'Shri Guru Gobind Singh Ji Airport', digiYatra: false },
  { code: 'JLG', city: 'Jalgaon', state: 'Maharashtra', country: 'India', name: 'Jalgaon Airport', digiYatra: false },
  { code: 'SDW', city: 'Sindhudurg (Chipi / Konkan)', state: 'Maharashtra', country: 'India', name: 'Sindhudurg Airport', digiYatra: false },
  { code: 'GOP', city: 'Gondia', state: 'Maharashtra', country: 'India', name: 'Birsi Airport', digiYatra: false },

  // --- KARNATAKA ---
  { code: 'IXE', city: 'Mangaluru (Mangalore)', state: 'Karnataka', country: 'India', name: 'Mangaluru International Airport (Bajpe)', digiYatra: false },
  { code: 'HBX', city: 'Hubballi (Hubli/Dharwad)', state: 'Karnataka', country: 'India', name: 'Hubballi Airport', digiYatra: false },
  { code: 'IXG', city: 'Belagavi (Belgaum)', state: 'Karnataka', country: 'India', name: 'Belagavi Airport (Sambre)', digiYatra: false },
  { code: 'MYQ', city: 'Mysuru (Mysore)', state: 'Karnataka', country: 'India', name: 'Mysuru Airport (Mandakalli)', digiYatra: false },
  { code: 'GBI', city: 'Kalaburagi (Gulbarga)', state: 'Karnataka', country: 'India', name: 'Kalaburagi Airport', digiYatra: false },
  { code: 'RQY', city: 'Shivamogga (Shimoga)', state: 'Karnataka', country: 'India', name: 'Kuvempu Airport (Sogane)', digiYatra: false },
  { code: 'VDY', city: 'Vidyanagar (Ballari/Hampi)', state: 'Karnataka', country: 'India', name: 'Jindal Vijaynagar Airport', digiYatra: false },
  { code: 'BDR', city: 'Bidar', state: 'Karnataka', country: 'India', name: 'Bidar Civil Airport', digiYatra: false },

  // --- TAMIL NADU & PUDUCHERRY ---
  { code: 'CJB', city: 'Coimbatore', state: 'Tamil Nadu', country: 'India', name: 'Coimbatore International Airport (Peelamedu)', digiYatra: false },
  { code: 'TRZ', city: 'Tiruchirappalli (Trichy)', state: 'Tamil Nadu', country: 'India', name: 'Tiruchirappalli International Airport (New Terminal)', digiYatra: false },
  { code: 'IXM', city: 'Madurai', state: 'Tamil Nadu', country: 'India', name: 'Madurai International Airport', digiYatra: false },
  { code: 'SXV', city: 'Salem', state: 'Tamil Nadu', country: 'India', name: 'Salem Airport (Kamalapuram)', digiYatra: false },
  { code: 'TCR', city: 'Tuticorin (Thoothukudi)', state: 'Tamil Nadu', country: 'India', name: 'Tuticorin Airport (Vagaikulam)', digiYatra: false },
  { code: 'NVY', city: 'Neyveli', state: 'Tamil Nadu', country: 'India', name: 'Neyveli Airport', digiYatra: false },
  { code: 'PNY', city: 'Puducherry (Pondicherry)', state: 'Puducherry', country: 'India', name: 'Pondicherry Airport (Lawspet)', digiYatra: false },

  // --- KERALA & LAKSHADWEEP ---
  { code: 'COK', city: 'Kochi (Cochin)', state: 'Kerala', country: 'India', name: 'Cochin International Airport (Nedumbassery - Solar)', digiYatra: true, popular: true },
  { code: 'TRV', city: 'Thiruvananthapuram (Trivandrum)', state: 'Kerala', country: 'India', name: 'Trivandrum International Airport (Chacka/Valiyathura)', digiYatra: false },
  { code: 'CCJ', city: 'Kozhikode (Calicut)', state: 'Kerala', country: 'India', name: 'Calicut International Airport (Karipur)', digiYatra: false },
  { code: 'CNN', city: 'Kannur', state: 'Kerala', country: 'India', name: 'Kannur International Airport (Mattannur)', digiYatra: false },
  { code: 'AGX', city: 'Agatti Island', state: 'Lakshadweep', country: 'India', name: 'Agatti Island Airport (Coral Atoll)', digiYatra: false, popular: true },

  // --- TELANGANA & ANDHRA PRADESH ---
  { code: 'WGC', city: 'Warangal', state: 'Telangana', country: 'India', name: 'Mamnoor Airport', digiYatra: false },
  { code: 'VTZ', city: 'Visakhapatnam (Vizag)', state: 'Andhra Pradesh', country: 'India', name: 'Visakhapatnam International Airport (INS Dega)', digiYatra: true },
  { code: 'VGA', city: 'Vijayawada (Amaravati)', state: 'Andhra Pradesh', country: 'India', name: 'Vijayawada International Airport (Gannavaram)', digiYatra: true },
  { code: 'TIR', city: 'Tirupati (Balaji)', state: 'Andhra Pradesh', country: 'India', name: 'Tirupati International Airport (Renigunta)', digiYatra: false, popular: true },
  { code: 'RJA', city: 'Rajahmundry', state: 'Andhra Pradesh', country: 'India', name: 'Rajahmundry Airport (Madhurapudi)', digiYatra: false },
  { code: 'KJB', city: 'Kurnool', state: 'Andhra Pradesh', country: 'India', name: 'Uyyalawada Narasimha Reddy Airport (Orvakal)', digiYatra: false },
  { code: 'CDP', city: 'Kadapa', state: 'Andhra Pradesh', country: 'India', name: 'Kadapa Airport', digiYatra: false },
  { code: 'PUT', city: 'Puttaparthi', state: 'Andhra Pradesh', country: 'India', name: 'Sri Sathya Sai Airport', digiYatra: false },

  // --- WEST BENGAL, ODISHA, BIHAR & JHARKHAND ---
  { code: 'IXB', city: 'Bagdogra (Siliguri/Darjeeling)', state: 'West Bengal', country: 'India', name: 'Bagdogra International Airport', digiYatra: false, popular: true },
  { code: 'RDP', city: 'Durgapur (Asansol)', state: 'West Bengal', country: 'India', name: 'Kazi Nazrul Islam Airport (Andal)', digiYatra: false },
  { code: 'COH', city: 'Cooch Behar', state: 'West Bengal', country: 'India', name: 'Cooch Behar Airport', digiYatra: false },
  { code: 'BBI', city: 'Bhubaneswar', state: 'Odisha', country: 'India', name: 'Biju Patnaik International Airport (T1/T2)', digiYatra: true },
  { code: 'JRG', city: 'Jharsuguda', state: 'Odisha', country: 'India', name: 'Veer Surendra Sai Airport', digiYatra: false },
  { code: 'RRK', city: 'Rourkela', state: 'Odisha', country: 'India', name: 'Rourkela Steel City Airport', digiYatra: false },
  { code: 'PYB', city: 'Jeypore', state: 'Odisha', country: 'India', name: 'Jeypore Airport', digiYatra: false },
  { code: 'UTK', city: 'Utkela (Kalahandi)', state: 'Odisha', country: 'India', name: 'Utkela Airport', digiYatra: false },
  { code: 'PAT', city: 'Patna', state: 'Bihar', country: 'India', name: 'Jay Prakash Narayan Airport', digiYatra: true },
  { code: 'GAY', city: 'Gaya (Bodh Gaya)', state: 'Bihar', country: 'India', name: 'Gaya International Airport (Buddhist Circuit)', digiYatra: false },
  { code: 'DBR', city: 'Darbhanga', state: 'Bihar', country: 'India', name: 'Darbhanga Airport (Mithila Region)', digiYatra: false },
  { code: 'IXR', city: 'Ranchi', state: 'Jharkhand', country: 'India', name: 'Birsa Munda Airport (Hinoo)', digiYatra: false },
  { code: 'DGO', city: 'Deoghar (Baidyanath)', state: 'Jharkhand', country: 'India', name: 'Deoghar International Airport', digiYatra: false, popular: true },
  { code: 'JSR', city: 'Jamshedpur', state: 'Jharkhand', country: 'India', name: 'Sonari Airport', digiYatra: false },

  // --- MADHYA PRADESH & CHHATTISGARH ---
  { code: 'IDR', city: 'Indore', state: 'Madhya Pradesh', country: 'India', name: 'Devi Ahilya Bai Holkar International Airport', digiYatra: false, popular: true },
  { code: 'BHO', city: 'Bhopal', state: 'Madhya Pradesh', country: 'India', name: 'Raja Bhoj International Airport (Gandhi Nagar)', digiYatra: false },
  { code: 'GWL', city: 'Gwalior', state: 'Madhya Pradesh', country: 'India', name: 'Rajmata Vijaya Raje Scindia Airport (New Terminal)', digiYatra: false },
  { code: 'JLR', city: 'Jabalpur', state: 'Madhya Pradesh', country: 'India', name: 'Dumna Airport (Marble Rocks)', digiYatra: false },
  { code: 'HJR', city: 'Khajuraho', state: 'Madhya Pradesh', country: 'India', name: 'Khajuraho Airport (UNESCO Temples)', digiYatra: false },
  { code: 'REW', city: 'Rewa', state: 'Madhya Pradesh', country: 'India', name: 'Rewa Airport (White Tiger Land)', digiYatra: false },
  { code: 'RPR', city: 'Raipur', state: 'Chhattisgarh', country: 'India', name: 'Swami Vivekananda International Airport (Mana)', digiYatra: false },
  { code: 'JGB', city: 'Jagdalpur (Bastar)', state: 'Chhattisgarh', country: 'India', name: 'Maa Danteshwari Airport', digiYatra: false },
  { code: 'PAB', city: 'Bilaspur', state: 'Chhattisgarh', country: 'India', name: 'Bilasa Devi Kevat Airport (Chakarbhata)', digiYatra: false },
  { code: 'RGH', city: 'Raigarh', state: 'Chhattisgarh', country: 'India', name: 'Raigarh Airport', digiYatra: false },
  { code: 'AGY', city: 'Ambikapur', state: 'Chhattisgarh', country: 'India', name: 'Maa Mahamaya Airport (Darima)', digiYatra: false },

  // --- NORTH-EASTERN STATES & SIKKIM ---
  { code: 'GAU', city: 'Guwahati', state: 'Assam', country: 'India', name: 'Lokpriya Gopinath Bordoloi International Airport (Borjhar)', digiYatra: true, popular: true },
  { code: 'DIB', city: 'Dibrugarh', state: 'Assam', country: 'India', name: 'Dibrugarh Airport (Mohanbari)', digiYatra: false },
  { code: 'IXS', city: 'Silchar', state: 'Assam', country: 'India', name: 'Silchar Airport (Kumbhirgram)', digiYatra: false },
  { code: 'JRH', city: 'Jorhat', state: 'Assam', country: 'India', name: 'Jorhat Airport (Rowriah Air Force)', digiYatra: false },
  { code: 'TEZ', city: 'Tezpur', state: 'Assam', country: 'India', name: 'Tezpur Airport (Salonibari)', digiYatra: false },
  { code: 'IXI', city: 'Lilabari (North Lakhimpur)', state: 'Assam', country: 'India', name: 'Lilabari Airport', digiYatra: false },
  { code: 'RUP', city: 'Rupsi (Dhubri)', state: 'Assam', country: 'India', name: 'Rupsi Airport', digiYatra: false },
  { code: 'HGI', city: 'Itanagar (Hollongi)', state: 'Arunachal Pradesh', country: 'India', name: 'Donyi Polo Airport (Greenfield Hub)', digiYatra: false },
  { code: 'PAS', city: 'Pasighat', state: 'Arunachal Pradesh', country: 'India', name: 'Pasighat Airport', digiYatra: false },
  { code: 'TEI', city: 'Tezu', state: 'Arunachal Pradesh', country: 'India', name: 'Tezu Airport', digiYatra: false },
  { code: 'ZER', city: 'Ziro', state: 'Arunachal Pradesh', country: 'India', name: 'Ziro Airport (Music Festival Valley)', digiYatra: false },
  { code: 'IMF', city: 'Imphal', state: 'Manipur', country: 'India', name: 'Bir Tikendrajit International Airport (Tulihal)', digiYatra: false },
  { code: 'SHL', city: 'Shillong', state: 'Meghalaya', country: 'India', name: 'Shillong Airport (Umroi/Barapani)', digiYatra: false },
  { code: 'AJL', city: 'Aizawl', state: 'Mizoram', country: 'India', name: 'Lengpui Airport (Tabletop Runway)', digiYatra: false },
  { code: 'DMU', city: 'Dimapur', state: 'Nagaland', country: 'India', name: 'Dimapur Airport', digiYatra: false },
  { code: 'IXA', city: 'Agartala', state: 'Tripura', country: 'India', name: 'Maharaja Bir Bikram Airport (Singerbhil)', digiYatra: false },
  { code: 'PYG', city: 'Pakyong (Gangtok)', state: 'Sikkim', country: 'India', name: 'Pakyong Airport (Himalayan Greenfield)', digiYatra: false, popular: true },

  // --- ANDAMAN & NICOBAR ISLANDS ---
  { code: 'IXZ', city: 'Port Blair', state: 'Andaman & Nicobar', country: 'India', name: 'Veer Savarkar International Airport (New Integrated Terminal)', digiYatra: false, popular: true },

  // --- KEY INTERNATIONAL CONNECTION GATEWAYS ---
  { code: 'DXB', city: 'Dubai', state: 'Dubai', country: 'UAE', name: 'Dubai International Airport (Direct from 20+ Indian Cities)', popular: true },
  { code: 'AUH', city: 'Abu Dhabi', state: 'Abu Dhabi', country: 'UAE', name: 'Zayed International Airport', popular: false },
  { code: 'DOH', city: 'Doha', state: 'Doha', country: 'Qatar', name: 'Hamad International Airport', popular: false },
  { code: 'SIN', city: 'Singapore', state: 'Singapore', country: 'Singapore', name: 'Singapore Changi Airport (T1/T2/T3/T4)', popular: true },
  { code: 'BKK', city: 'Bangkok', state: 'Bangkok', country: 'Thailand', name: 'Suvarnabhumi Airport', popular: true },
  { code: 'KUL', city: 'Kuala Lumpur', state: 'Selangor', country: 'Malaysia', name: 'Kuala Lumpur International Airport (KLIA/KLIA2)', popular: false },
  { code: 'CMB', city: 'Colombo', state: 'Western', country: 'Sri Lanka', name: 'Bandaranaike International Airport', popular: false },
  { code: 'MLE', city: 'Male', state: 'Kaafu', country: 'Maldives', name: 'Velana International Airport (Direct from India)', popular: true },
  { code: 'KTM', city: 'Kathmandu', state: 'Bagmati', country: 'Nepal', name: 'Tribhuvan International Airport', popular: false },
  { code: 'LHR', city: 'London', state: 'England', country: 'United Kingdom', name: 'London Heathrow Airport (Direct from DEL/BOM/BLR/MAA/HYD)', popular: true },
  { code: 'JFK', city: 'New York', state: 'New York', country: 'USA', name: 'John F. Kennedy International Airport (Air India Direct)', popular: false },
  { code: 'SFO', city: 'San Francisco', state: 'California', country: 'USA', name: 'San Francisco International Airport (Non-stop from DEL/BOM/BLR)', popular: false },
  { code: 'FRA', city: 'Frankfurt', state: 'Hesse', country: 'Germany', name: 'Frankfurt Airport', popular: false },
  { code: 'CDG', city: 'Paris', state: 'Île-de-France', country: 'France', name: 'Charles de Gaulle Airport', popular: false },
  { code: 'HND', city: 'Tokyo', state: 'Tokyo', country: 'Japan', name: 'Tokyo Haneda Airport', popular: false }
];

// Indian & Partner Airlines Reference List
const AIRLINES_LIST = [
  { code: '6E', name: 'IndiGo', logo: '6E', color: '#004b93' },
  { code: 'AI', name: 'Air India', logo: 'AI', color: '#e31837' },
  { code: 'UK', name: 'Vistara', logo: 'UK', color: '#581845' },
  { code: 'QP', name: 'Akasa Air', logo: 'QP', color: '#ff6200' },
  { code: 'SG', name: 'SpiceJet', logo: 'SG', color: '#f36c21' },
  { code: 'IX', name: 'Air India Express', logo: 'IX', color: '#ff3b00' },
  { code: 'FL', name: 'Flyora Skyways', logo: 'FL', color: '#00f2fe' }
];

// Curated Indian Destinations Data (Prices in INR)
const DESTINATIONS_DATA = [
  {
    city: 'Goa',
    country: 'India',
    iata: 'GOI',
    category: 'beaches',
    price: 3299,
    weather: '28°C Tropical & Sunny',
    image: 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80'
  },
  {
    city: 'Srinagar (Kashmir)',
    country: 'India',
    iata: 'SXR',
    category: 'mountains',
    price: 4499,
    weather: '14°C Cool & Scenic',
    image: 'https://images.unsplash.com/photo-1595815771614-ade9d652a65d?auto=format&fit=crop&w=800&q=80'
  },
  {
    city: 'Jaipur (Rajasthan)',
    country: 'India',
    iata: 'JAI',
    category: 'heritage',
    price: 2799,
    weather: '26°C Royal & Warm',
    image: 'https://images.unsplash.com/photo-1603262110263-fb010d6e75dc?auto=format&fit=crop&w=800&q=80'
  },
  {
    city: 'Kochi (Kerala)',
    country: 'India',
    iata: 'COK',
    category: 'nature',
    price: 3899,
    weather: '29°C Lush Backwaters',
    image: 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80'
  },
  {
    city: 'Varanasi',
    country: 'India',
    iata: 'VNS',
    category: 'spiritual',
    price: 2999,
    weather: '24°C Ganga Ghats',
    image: 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80'
  },
  {
    city: 'Leh Ladakh',
    country: 'India',
    iata: 'IXL',
    category: 'mountains',
    price: 5999,
    weather: '10°C Himalayan Splendor',
    image: 'https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=800&q=80'
  },
  {
    city: 'Mumbai',
    country: 'India',
    iata: 'BOM',
    category: 'metros',
    price: 3499,
    weather: '30°C Coastal City',
    image: 'https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80'
  },
  {
    city: 'Bengaluru',
    country: 'India',
    iata: 'BLR',
    category: 'metros',
    price: 3199,
    weather: '23°C Pleasant Breeze',
    image: 'https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80'
  },
  {
    city: 'Port Blair (Andaman)',
    country: 'India',
    iata: 'IXZ',
    category: 'beaches',
    price: 6499,
    weather: '29°C Island Bliss',
    image: 'https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=800&q=80'
  },
  {
    city: 'Kolkata',
    country: 'India',
    iata: 'CCU',
    category: 'metros',
    price: 3399,
    weather: '27°C Cultural Hub',
    image: 'https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=800&q=80'
  }
];

// ==========================================
// 2. INITIALIZATION & EVENT LISTENERS
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initDatePickers();
  initCurrencySelector();
  initTripTypeSelector();
  initFarePills();
  initPassengersPopover();
  initAutocomplete();
  initSwapLocations();
  initFilters();
  initSortTabs();
  initSearch();
  initFlightTracker();
  initDestinations();
  initModals();
  initAiCopilot();
  initMyTrips();
  initNewsletter();

  // Initial flight search generation (Delhi to Mumbai in INR)
  generateMockFlights();
  renderDestinations('all');
  updateTripsCountBadge();

  if (window.lucide) {
    lucide.createIcons();
  }
});

// Theme Management
function initTheme() {
  document.documentElement.setAttribute('data-theme', AppState.theme);
  const themeBtn = document.getElementById('themeToggleBtn');
  themeBtn.addEventListener('click', () => {
    AppState.theme = AppState.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', AppState.theme);
    localStorage.setItem('flyora_theme', AppState.theme);
    showToast(`Switched to ${AppState.theme.toUpperCase()} mode`, 'info');
  });
}

// Date Pickers initialization
function initDatePickers() {
  const departInput = document.getElementById('departDateInput');
  const returnInput = document.getElementById('returnDateInput');
  
  const today = new Date().toISOString().split('T')[0];
  departInput.min = today;
  returnInput.min = today;

  departInput.value = AppState.search.departDate;
  returnInput.value = AppState.search.returnDate;

  departInput.addEventListener('change', (e) => {
    AppState.search.departDate = e.target.value;
    returnInput.min = e.target.value;
    updateDayNames();
  });

  returnInput.addEventListener('change', (e) => {
    AppState.search.returnDate = e.target.value;
    updateDayNames();
  });

  updateDayNames();
}

function updateDayNames() {
  const departInput = document.getElementById('departDateInput');
  const returnInput = document.getElementById('returnDateInput');
  const depLbl = document.getElementById('departDayName');
  const retLbl = document.getElementById('returnDayName');

  if (departInput && departInput.value) {
    const d = new Date(departInput.value);
    depLbl.textContent = d.toLocaleDateString('en-IN', { weekday: 'short', month: 'short', day: 'numeric' });
  }
  if (returnInput && returnInput.value) {
    const d = new Date(returnInput.value);
    retLbl.textContent = d.toLocaleDateString('en-IN', { weekday: 'short', month: 'short', day: 'numeric' });
  }
}

// Currency Selector (Default INR)
function initCurrencySelector() {
  const dropdown = document.getElementById('currencyDropdown');
  const btn = document.getElementById('currencyBtn');
  const items = dropdown.querySelectorAll('.dropdown-item');

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.classList.toggle('open');
  });

  document.addEventListener('click', () => dropdown.classList.remove('open'));

  items.forEach(item => {
    item.addEventListener('click', () => {
      items.forEach(i => i.classList.remove('active'));
      item.classList.add('active');

      AppState.currency = {
        code: item.getAttribute('data-currency'),
        symbol: item.getAttribute('data-symbol'),
        rate: parseFloat(item.getAttribute('data-rate')),
        flag: item.getAttribute('data-flag')
      };

      document.getElementById('currentCurrencyFlag').textContent = AppState.currency.flag;
      document.getElementById('currentCurrencyCode').textContent = `${AppState.currency.code} (${AppState.currency.symbol.trim()})`;
      dropdown.classList.remove('open');

      // Refresh prices across the app
      renderFlightCards();
      renderDestinations(document.querySelector('.dest-tab.active')?.getAttribute('data-category') || 'all');
      showToast(`Currency changed to ${AppState.currency.code}`, 'info');
    });
  });
}

// Format Price with Indian Currency Notation
function formatCurrency(inrBasePrice) {
  const converted = Math.round(inrBasePrice * AppState.currency.rate);
  if (AppState.currency.code === 'INR') {
    return `₹${converted.toLocaleString('en-IN')}`;
  }
  return `${AppState.currency.symbol}${converted.toLocaleString()}`;
}

// ==========================================
// 3. SEARCH ENGINE & INPUT CONTROLS
// ==========================================
function initTripTypeSelector() {
  const buttons = document.querySelectorAll('.trip-type-btn');
  const returnDateCard = document.getElementById('returnDateCard');
  const returnDateInput = document.getElementById('returnDateInput');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const tripType = btn.getAttribute('data-trip');
      AppState.search.tripType = tripType;

      if (tripType === 'round-trip') {
        returnDateCard.classList.remove('disabled');
        returnDateInput.removeAttribute('disabled');
        returnDateInput.setAttribute('required', 'true');
      } else {
        returnDateCard.classList.add('disabled');
        returnDateInput.setAttribute('disabled', 'true');
        returnDateInput.removeAttribute('required');
      }

      if (tripType === 'multi-city') {
        showToast('Multi-city planner active. Pick your primary Indian segment.', 'info');
      }
    });
  });
}

function initFarePills() {
  const pills = document.querySelectorAll('.fare-pill');
  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      const radio = pill.querySelector('input');
      radio.checked = true;
      AppState.search.fareType = radio.value;
      generateMockFlights();
    });
  });
}

function initPassengersPopover() {
  const displayBtn = document.getElementById('passengerDisplayBtn');
  const card = document.getElementById('passengerCard');
  const popover = document.getElementById('passengersPopover');
  const applyBtn = document.getElementById('applyPaxBtn');
  const steppers = popover.querySelectorAll('.step-btn');
  const cabinPills = popover.querySelectorAll('.cabin-pill');

  displayBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    card.classList.toggle('open');
  });

  document.addEventListener('click', (e) => {
    if (!card.contains(e.target)) {
      card.classList.remove('open');
    }
  });

  steppers.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const type = btn.getAttribute('data-type');
      const dir = parseInt(btn.getAttribute('data-dir'));
      const countEl = document.getElementById(`${type}Count`);
      let currentVal = AppState.search.passengers[type];
      let newVal = currentVal + dir;

      if (type === 'adult' && newVal < 1) newVal = 1;
      if ((type === 'child' || type === 'infant') && newVal < 0) newVal = 0;
      if (newVal > 9) newVal = 9;

      AppState.search.passengers[type] = newVal;
      countEl.textContent = newVal;
      updatePaxDisplaySummary();
    });
  });

  cabinPills.forEach(pill => {
    pill.addEventListener('click', () => {
      cabinPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      const radio = pill.querySelector('input');
      radio.checked = true;
      AppState.search.cabinClass = radio.value;
      updatePaxDisplaySummary();
    });
  });

  applyBtn.addEventListener('click', () => {
    card.classList.remove('open');
    generateMockFlights();
  });
}

function updatePaxDisplaySummary() {
  const total = AppState.search.passengers.adult + AppState.search.passengers.child + AppState.search.passengers.infant;
  const label = total === 1 ? '1 Traveler' : `${total} Travelers`;
  const cabinFormatted = AppState.search.cabinClass.charAt(0).toUpperCase() + AppState.search.cabinClass.slice(1);
  
  document.getElementById('totalTravelersCount').textContent = label;
  document.getElementById('summaryCabinClass').textContent = cabinFormatted;
  document.getElementById('cabinClassLabel').textContent = cabinFormatted;
}

// Autocomplete Airport Search
function initAutocomplete() {
  setupAirportInput('originInput', 'originDropdown', 'originCodeBadge', (airport) => {
    AppState.search.origin = airport;
  });

  setupAirportInput('destInput', 'destDropdown', 'destCodeBadge', (airport) => {
    AppState.search.destination = airport;
  });
}

function setupAirportInput(inputId, dropdownId, badgeId, onSelect) {
  const input = document.getElementById(inputId);
  const dropdown = document.getElementById(dropdownId);
  const badge = document.getElementById(badgeId);
  const wrapper = input.closest('.autocomplete-wrapper');

  input.addEventListener('focus', () => {
    renderDropdownOptions(input.value.trim(), dropdown, (airport) => {
      input.value = `${airport.city} (${airport.code})`;
      badge.textContent = airport.code;
      wrapper.classList.remove('active');
      onSelect(airport);
    });
    wrapper.classList.add('active');
  });

  input.addEventListener('input', () => {
    renderDropdownOptions(input.value.trim(), dropdown, (airport) => {
      input.value = `${airport.city} (${airport.code})`;
      badge.textContent = airport.code;
      wrapper.classList.remove('active');
      onSelect(airport);
    });
  });

  document.addEventListener('click', (e) => {
    if (!wrapper.contains(e.target)) {
      wrapper.classList.remove('active');
    }
  });
}

function renderDropdownOptions(query, container, onSelect) {
  const q = query.toLowerCase().trim();
  container.innerHTML = '';

  let matched = [];
  let isDefaultSuggestions = false;

  if (!q || q.length === 0) {
    // Show top popular Indian airports by default
    matched = AIRPORTS.filter(a => a.popular);
    isDefaultSuggestions = true;
  } else {
    // Intelligent search across city, state, code, and airport name
    matched = AIRPORTS.filter(a => 
      a.code.toLowerCase().includes(q) ||
      a.city.toLowerCase().includes(q) || 
      (a.state && a.state.toLowerCase().includes(q)) ||
      a.country.toLowerCase().includes(q) ||
      a.name.toLowerCase().includes(q)
    );

    // Rank exact matches higher
    matched.sort((a, b) => {
      const aCode = a.code.toLowerCase() === q;
      const bCode = b.code.toLowerCase() === q;
      if (aCode && !bCode) return -1;
      if (!aCode && bCode) return 1;

      const aCity = a.city.toLowerCase().startsWith(q);
      const bCity = b.city.toLowerCase().startsWith(q);
      if (aCity && !bCity) return -1;
      if (!aCity && bCity) return 1;

      return 0;
    });
  }

  if (matched.length === 0) {
    container.innerHTML = '<div style="padding: 12px 10px; color: var(--text-muted); font-size: 0.85rem; text-align: center;"><i data-lucide="map-pin-off" style="width: 18px; height: 18px; margin-bottom: 4px; display: block; margin: 0 auto 4px auto;"></i>No matching Indian airport found. Try searching by city, state, or 3-letter IATA code.</div>';
    if (window.lucide) lucide.createIcons();
    return;
  }

  // Section Header
  const header = document.createElement('div');
  header.className = 'dropdown-section-header';
  header.textContent = isDefaultSuggestions ? '⭐ Popular Indian Airports' : `Found ${matched.length} Airport${matched.length === 1 ? '' : 's'}`;
  container.appendChild(header);

  // Render top 12 results with scrollable container
  matched.slice(0, 12).forEach(airport => {
    const item = document.createElement('div');
    item.className = 'airport-result-item';
    
    const stateBadge = airport.state ? `<span class="airport-state-badge">${airport.state}</span>` : `<span class="airport-state-badge">${airport.country}</span>`;
    const digiYatraTag = airport.digiYatra ? `<span class="digiyatra-tag"><i data-lucide="shield-check"></i> DigiYatra</span>` : '';

    item.innerHTML = `
      <div class="airport-meta">
        <div class="airport-city-row">
          <span class="airport-city-name">${airport.city}</span>
          ${stateBadge}
          ${digiYatraTag}
        </div>
        <span class="airport-full-name">${airport.name}</span>
      </div>
      <span class="airport-iata-pill">${airport.code}</span>
    `;
    
    item.addEventListener('click', () => onSelect(airport));
    container.appendChild(item);
  });

  if (window.lucide) lucide.createIcons();
}

// Swap Origin & Destination
function initSwapLocations() {
  const swapBtn = document.getElementById('swapLocationsBtn');
  swapBtn.addEventListener('click', () => {
    const temp = AppState.search.origin;
    AppState.search.origin = AppState.search.destination;
    AppState.search.destination = temp;

    document.getElementById('originInput').value = `${AppState.search.origin.city} (${AppState.search.origin.code})`;
    document.getElementById('originCodeBadge').textContent = AppState.search.origin.code;

    document.getElementById('destInput').value = `${AppState.search.destination.city} (${AppState.search.destination.code})`;
    document.getElementById('destCodeBadge').textContent = AppState.search.destination.code;

    generateMockFlights();
    showToast(`Swapped route: ${AppState.search.origin.code} ➔ ${AppState.search.destination.code}`, 'info');
  });
}

// Quick Trending Route Chips
document.querySelectorAll('.quick-route-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    const fromCode = chip.getAttribute('data-from');
    const toCode = chip.getAttribute('data-to');

    const fromAirport = AIRPORTS.find(a => a.code === fromCode) || { code: fromCode, city: fromCode, name: fromCode, country: 'India' };
    const toAirport = AIRPORTS.find(a => a.code === toCode) || { code: toCode, city: toCode, name: toCode, country: 'India' };

    AppState.search.origin = fromAirport;
    AppState.search.destination = toAirport;

    document.getElementById('originInput').value = `${fromAirport.city} (${fromAirport.code})`;
    document.getElementById('originCodeBadge').textContent = fromAirport.code;

    document.getElementById('destInput').value = `${toAirport.city} (${toAirport.code})`;
    document.getElementById('destCodeBadge').textContent = toAirport.code;

    generateMockFlights();
    scrollToResults();
  });
});

function initSearch() {
  const searchBtn = document.getElementById('searchFlightsBtn');
  searchBtn.addEventListener('click', () => {
    generateMockFlights();
    scrollToResults();
    showToast('Found real-time Indian flights with DigiYatra seat availability!', 'success');
  });
}

function scrollToResults() {
  document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

// ==========================================
// 4. FLIGHT GENERATION & FILTER ENGINE (INR)
// ==========================================
function generateMockFlights() {
  const origin = AppState.search.origin;
  const dest = AppState.search.destination;
  const cabinMultiplier = { economy: 1, premium: 1.55, business: 2.8, first: 4.5 }[AppState.search.cabinClass] || 1;
  const fareDiscount = AppState.search.fareType === 'student' ? 0.88 : (AppState.search.fareType === 'senior' ? 0.85 : (AppState.search.fareType === 'armed' ? 0.80 : 1));

  // Authentic Indian Flight Templates (Prices in INR)
  const flightTemplates = [
    {
      id: '6E-205',
      airline: AIRLINES_LIST[0], // IndiGo
      depTime: '06:15 AM',
      arrTime: '08:30 AM',
      duration: '2h 15m',
      durationMinutes: 135,
      stops: 0,
      basePrice: 3499,
      aircraft: 'Airbus A321neo',
      emissions: '140 kg CO₂ (Eco-Friendly Fleet)',
      hasWifi: true,
      hasPower: true,
      hasMeal: false,
      baggage: '1 Cabin (7kg) + 1 Checked (15kg)',
      cancellation: 'DGCA 24h Free Cancellation / Instant Refund'
    },
    {
      id: 'AI-882',
      airline: AIRLINES_LIST[1], // Air India
      depTime: '08:45 AM',
      arrTime: '11:00 AM',
      duration: '2h 15m',
      durationMinutes: 135,
      stops: 0,
      basePrice: 3950,
      aircraft: 'Airbus A320neo (New Cabin)',
      emissions: '155 kg CO₂',
      hasWifi: true,
      hasPower: true,
      hasMeal: true,
      baggage: '1 Cabin (7kg) + 1 Checked (15kg) + Hot Meal',
      cancellation: 'Refundable with ₹500 fee'
    },
    {
      id: 'UK-994',
      airline: AIRLINES_LIST[2], // Vistara
      depTime: '11:30 AM',
      arrTime: '01:45 PM',
      duration: '2h 15m',
      durationMinutes: 135,
      stops: 0,
      basePrice: 4250,
      aircraft: 'Airbus A321neo Premium',
      emissions: '148 kg CO₂',
      hasWifi: true,
      hasPower: true,
      hasMeal: true,
      baggage: '1 Cabin (7kg) + 1 Checked (15kg) + Gourmet Dining',
      cancellation: 'Free cancellation within 24 hours'
    },
    {
      id: 'QP-1102',
      airline: AIRLINES_LIST[3], // Akasa Air
      depTime: '02:40 PM',
      arrTime: '04:55 PM',
      duration: '2h 15m',
      durationMinutes: 135,
      stops: 0,
      basePrice: 3299,
      aircraft: 'Boeing 737 MAX 8',
      emissions: '135 kg CO₂ (-20% Eco Fuel)',
      hasWifi: false,
      hasPower: true,
      hasMeal: false,
      baggage: '1 Cabin (7kg) + 1 Checked (15kg)',
      cancellation: 'Instant UPI refund guarantee'
    },
    {
      id: 'SG-302',
      airline: AIRLINES_LIST[4], // SpiceJet
      depTime: '05:50 PM',
      arrTime: '09:20 PM',
      duration: '3h 30m',
      durationMinutes: 210,
      stops: 1,
      layoverCity: 'Jaipur (JAI)',
      layoverDuration: '45m',
      basePrice: 2899,
      aircraft: 'Boeing 737-800',
      emissions: '160 kg CO₂',
      hasWifi: false,
      hasPower: false,
      hasMeal: false,
      baggage: '1 Cabin (7kg) + 1 Checked (15kg)',
      cancellation: 'Non-refundable saver fare'
    },
    {
      id: 'IX-420',
      airline: AIRLINES_LIST[5], // Air India Express
      depTime: '08:15 PM',
      arrTime: '10:30 PM',
      duration: '2h 15m',
      durationMinutes: 135,
      stops: 0,
      basePrice: 3150,
      aircraft: 'Boeing 737 MAX 8',
      emissions: '138 kg CO₂',
      hasWifi: true,
      hasPower: true,
      hasMeal: true,
      baggage: '1 Cabin (7kg) + 1 Checked (15kg)',
      cancellation: 'DGCA free 24h cancellation'
    }
  ];

  AppState.currentFlights = flightTemplates.map(f => {
    const calculatedPrice = Math.round(f.basePrice * cabinMultiplier * fareDiscount);
    return {
      ...f,
      price: calculatedPrice,
      origin: origin.code,
      destination: dest.code,
      originCity: origin.city,
      destCity: dest.city
    };
  });

  // Setup dynamic airline filter options in sidebar
  renderAirlineFilterOptions();
  applyFiltersAndSort();
}

function renderAirlineFilterOptions() {
  const container = document.getElementById('airlineFilterList');
  if (!container) return;
  container.innerHTML = '';

  const uniqueAirlines = [...new Set(AppState.currentFlights.map(f => f.airline.name))];
  uniqueAirlines.forEach(name => {
    const label = document.createElement('label');
    label.className = 'custom-checkbox';
    label.innerHTML = `
      <input type="checkbox" name="airlineFilter" value="${name}" checked>
      <span class="checkmark"></span>
      <span class="cb-label">${name}</span>
    `;
    label.querySelector('input').addEventListener('change', applyFiltersAndSort);
    container.appendChild(label);
  });
}

function initFilters() {
  const priceSlider = document.getElementById('priceRangeInput');
  const priceDisplay = document.getElementById('priceFilterDisplay');
  const resetBtn = document.getElementById('resetFiltersBtn');
  const stopsCheckboxes = document.querySelectorAll('input[name="stopsFilter"]');
  const timeSlotBtns = document.querySelectorAll('.time-slot-btn');
  const wifiFilter = document.getElementById('wifiFilter');
  const powerFilter = document.getElementById('powerFilter');
  const mealFilter = document.getElementById('freeMealFilter');

  priceSlider.addEventListener('input', (e) => {
    AppState.filters.maxPrice = parseInt(e.target.value);
    priceDisplay.textContent = formatCurrency(AppState.filters.maxPrice);
    applyFiltersAndSort();
  });

  stopsCheckboxes.forEach(cb => cb.addEventListener('change', applyFiltersAndSort));

  timeSlotBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      timeSlotBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      AppState.filters.timeSlot = btn.getAttribute('data-slot');
      applyFiltersAndSort();
    });
  });

  if (wifiFilter) wifiFilter.addEventListener('change', applyFiltersAndSort);
  if (powerFilter) powerFilter.addEventListener('change', applyFiltersAndSort);
  if (mealFilter) mealFilter.addEventListener('change', applyFiltersAndSort);

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      priceSlider.value = 30000;
      AppState.filters.maxPrice = 30000;
      priceDisplay.textContent = formatCurrency(30000);

      stopsCheckboxes.forEach(cb => cb.checked = true);
      document.querySelectorAll('input[name="airlineFilter"]').forEach(cb => cb.checked = true);
      
      timeSlotBtns.forEach(b => b.classList.remove('active'));
      timeSlotBtns[0].classList.add('active');
      AppState.filters.timeSlot = 'all';

      if (wifiFilter) wifiFilter.checked = false;
      if (powerFilter) powerFilter.checked = false;
      if (mealFilter) mealFilter.checked = false;

      applyFiltersAndSort();
      showToast('Filters reset to default', 'info');
    });
  }
}

function initSortTabs() {
  const tabs = document.querySelectorAll('.sort-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      AppState.sortBy = tab.getAttribute('data-sort');
      applyFiltersAndSort();
    });
  });
}

function applyFiltersAndSort() {
  const checkedStops = Array.from(document.querySelectorAll('input[name="stopsFilter"]:checked')).map(cb => cb.value);
  const checkedAirlines = Array.from(document.querySelectorAll('input[name="airlineFilter"]:checked')).map(cb => cb.value);
  const wifiOnly = document.getElementById('wifiFilter')?.checked;
  const powerOnly = document.getElementById('powerFilter')?.checked;
  const mealOnly = document.getElementById('freeMealFilter')?.checked;

  let filtered = AppState.currentFlights.filter(f => {
    if (f.price > AppState.filters.maxPrice) return false;
    if (!checkedStops.includes(f.stops.toString())) return false;
    if (checkedAirlines.length > 0 && !checkedAirlines.includes(f.airline.name)) return false;
    if (wifiOnly && !f.hasWifi) return false;
    if (powerOnly && !f.hasPower) return false;
    if (mealOnly && !f.hasMeal) return false;

    // Time slot filter
    if (AppState.filters.timeSlot !== 'all') {
      const isAM = f.depTime.includes('AM');
      const hour = parseInt(f.depTime.split(':')[0]);
      if (AppState.filters.timeSlot === 'morning' && (!isAM || hour < 6 || hour === 12)) return false;
      if (AppState.filters.timeSlot === 'afternoon' && (isAM || hour >= 6)) return false;
      if (AppState.filters.timeSlot === 'evening' && (!isAM || hour >= 6) && (isAM || hour < 6)) return false;
    }

    return true;
  });

  // Sorting
  if (AppState.sortBy === 'cheapest') {
    filtered.sort((a, b) => a.price - b.price);
  } else if (AppState.sortBy === 'fastest') {
    filtered.sort((a, b) => a.durationMinutes - b.durationMinutes);
  } else if (AppState.sortBy === 'earliest') {
    filtered.sort((a, b) => a.depTime.localeCompare(b.depTime));
  } else if (AppState.sortBy === 'best') {
    // Smart AI balance: price and duration
    filtered.sort((a, b) => (a.price * 0.7 + a.durationMinutes * 0.3) - (b.price * 0.7 + b.durationMinutes * 0.3));
  }

  renderFlightCards(filtered);
  updateResultsSummary(filtered);
}

function updateResultsSummary(filtered) {
  const origin = AppState.search.origin;
  const dest = AppState.search.destination;
  document.getElementById('resultsTitle').textContent = `Flights from ${origin.city} to ${dest.city}`;

  if (filtered.length > 0) {
    const minPrice = Math.min(...filtered.map(f => f.price));
    const fastestDuration = filtered.reduce((min, f) => f.durationMinutes < min.durationMinutes ? f : min, filtered[0]).duration;
    const directCount = filtered.filter(f => f.stops === 0).length;

    document.getElementById('cheapestStatVal').textContent = formatCurrency(minPrice);
    document.getElementById('fastestStatVal').textContent = fastestDuration;
    document.getElementById('directCountVal').textContent = `${directCount} available`;
    document.getElementById('sortCheapestPrice').textContent = `from ${formatCurrency(minPrice)}`;
  } else {
    document.getElementById('cheapestStatVal').textContent = '—';
    document.getElementById('fastestStatVal').textContent = '—';
    document.getElementById('directCountVal').textContent = '0';
  }
}

function renderFlightCards(flights = AppState.currentFlights) {
  const container = document.getElementById('flightCardsContainer');
  if (!container) return;
  container.innerHTML = '';

  if (!flights || flights.length === 0) {
    container.innerHTML = `
      <div class="glass-panel" style="padding: 40px; text-align: center;">
        <i data-lucide="plane-off" style="width: 48px; height: 48px; color: var(--text-muted); margin-bottom: 12px;"></i>
        <h3>No flights match your filters</h3>
        <p style="color: var(--text-secondary); margin-top: 6px;">Try adjusting your price range in ₹, airlines, or stop filters.</p>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
    return;
  }

  flights.forEach((flight, index) => {
    const isBest = index === 0 && AppState.sortBy === 'best';
    const card = document.createElement('div');
    card.className = `flight-card glass-panel ${isBest ? 'best-deal' : ''}`;
    
    card.innerHTML = `
      <div class="flight-card-main">
        <!-- Airline -->
        <div class="airline-info-col">
          <div class="airline-logo-wrap" style="color: ${flight.airline.color};">
            ${flight.airline.logo}
          </div>
          <div class="airline-text-meta">
            <span class="airline-name">${flight.airline.name}</span>
            <span class="flight-code">${flight.id} • ${flight.aircraft}</span>
          </div>
        </div>

        <!-- Route Visualization -->
        <div class="flight-route-col">
          <div class="route-stop-block">
            <span class="route-time">${flight.depTime}</span>
            <span class="route-airport-code">${flight.origin}</span>
            <span class="route-city">${flight.originCity}</span>
          </div>

          <div class="route-duration-visual">
            <span class="duration-text">${flight.duration}</span>
            <div class="flight-path-bar">
              <div class="flight-plane-pin"><i data-lucide="plane"></i></div>
            </div>
            <span class="stop-type-badge ${flight.stops === 0 ? 'direct' : 'layover'}">
              ${flight.stops === 0 ? 'Non-Stop Direct' : `1 Stop (${flight.layoverCity})`}
            </span>
          </div>

          <div class="route-stop-block">
            <span class="route-time">${flight.arrTime}</span>
            <span class="route-airport-code">${flight.destination}</span>
            <span class="route-city">${flight.destCity}</span>
          </div>
        </div>

        <!-- Pricing & Book Action (INR) -->
        <div class="flight-price-col">
          <div class="price-unit-wrap">
            <span class="fare-per-pax">per traveler</span>
            <span class="price-main-amount">${formatCurrency(flight.price)}</span>
          </div>
          <button class="btn btn-primary select-flight-btn" data-flight-id="${flight.id}">
            Book Flight <i data-lucide="arrow-right"></i>
          </button>
        </div>
      </div>

      <!-- Card Bottom Features & Details Toggle -->
      <div class="flight-card-bottom">
        <div class="amenities-pills">
          ${flight.hasWifi ? '<span class="amenity-item"><i data-lucide="wifi"></i> Wi-Fi</span>' : ''}
          ${flight.hasPower ? '<span class="amenity-item"><i data-lucide="zap"></i> USB Power</span>' : ''}
          ${flight.hasMeal ? '<span class="amenity-item"><i data-lucide="utensils"></i> Hot Meal Included</span>' : ''}
          <span class="amenity-item"><i data-lucide="leaf"></i> ${flight.emissions}</span>
          <span class="amenity-item"><i data-lucide="shield-check"></i> DigiYatra Ready</span>
        </div>
        <button class="details-toggle-btn">
          <span>Flight Details</span> <i data-lucide="chevron-down"></i>
        </button>
      </div>

      <!-- Expandable Details Tab -->
      <div class="flight-card-expanded">
        <div class="expanded-grid">
          <div class="expanded-item">
            <strong>Baggage Allowance (DGCA)</strong>
            <span>${flight.baggage}</span>
          </div>
          <div class="expanded-item">
            <strong>Aircraft Fleet</strong>
            <span>${flight.aircraft}</span>
          </div>
          <div class="expanded-item">
            <strong>Cancellation & Changes</strong>
            <span>${flight.cancellation}</span>
          </div>
        </div>
      </div>
    `;

    // Toggle Details Tab
    const detailsBtn = card.querySelector('.details-toggle-btn');
    detailsBtn.addEventListener('click', () => card.classList.toggle('open'));

    // Select Flight Button
    const selectBtn = card.querySelector('.select-flight-btn');
    selectBtn.addEventListener('click', () => startBookingFlow(flight));

    container.appendChild(card);
  });

  if (window.lucide) lucide.createIcons();
}

// ==========================================
// 5. MULTI-STEP BOOKING & CABIN SEAT SELECTOR
// ==========================================
function startBookingFlow(flight) {
  AppState.selectedFlight = flight;
  AppState.booking.step = 1;
  AppState.booking.selectedSeat = '14B';
  AppState.booking.selectedSeatPrice = 0;

  // Update summary badges
  document.getElementById('modalFlightSummary').textContent = `${flight.airline.name} ${flight.id} • ${flight.originCity} (${flight.origin}) ➔ ${flight.destCity} (${flight.destination})`;
  document.getElementById('miniFlightAirline').textContent = `${flight.airline.name} (${flight.aircraft})`;
  document.getElementById('miniBaseFare').textContent = formatCurrency(flight.price);

  updateModalStepView();
  renderAirplaneCabinSeatMap();
  updateModalTotals();

  document.getElementById('bookingModalOverlay').classList.add('active');
}

function initModals() {
  const overlay = document.getElementById('bookingModalOverlay');
  const closeBtn = document.getElementById('closeBookingModalBtn');
  const backBtn = document.getElementById('modalBackBtn');
  const nextBtn = document.getElementById('modalNextBtn');

  closeBtn.addEventListener('click', () => overlay.classList.remove('active'));

  backBtn.addEventListener('click', () => {
    if (AppState.booking.step > 1) {
      AppState.booking.step--;
      updateModalStepView();
    }
  });

  nextBtn.addEventListener('click', () => {
    if (AppState.booking.step === 1) {
      // Validate Passenger form
      const firstName = document.getElementById('paxFirstName').value.trim();
      const lastName = document.getElementById('paxLastName').value.trim();
      const email = document.getElementById('paxEmail').value.trim();
      const phone = document.getElementById('paxPhone').value.trim();

      if (!firstName || !lastName || !email || !phone) {
        showToast('Please complete all required passenger fields for DigiYatra.', 'error');
        return;
      }

      AppState.booking.paxDetails = {
        firstName,
        lastName,
        email,
        phone,
        nationality: document.getElementById('paxNationality').value,
        dob: document.getElementById('paxDob').value,
        passport: document.getElementById('paxPassport').value || 'XXXX-XXXX-4892'
      };

      AppState.booking.step = 2;
      updateModalStepView();
    } else if (AppState.booking.step === 2) {
      AppState.booking.step = 3;
      updateModalStepView();
    } else if (AppState.booking.step === 3) {
      // Collect Addons
      AppState.booking.addons.baggage = document.getElementById('addonBaggageCheck').checked;
      AppState.booking.addons.meal = document.getElementById('addonMealCheck').checked;
      AppState.booking.addons.priority = document.getElementById('addonPriorityCheck').checked;
      AppState.booking.addons.insurance = document.getElementById('addonInsuranceCheck').checked;
      AppState.booking.addons.carbon = document.getElementById('addonCarbonCheck').checked;

      populateCheckoutSummary();
      AppState.booking.step = 4;
      updateModalStepView();
    } else if (AppState.booking.step === 4) {
      // Complete booking
      completeBooking();
    }
  });

  // Payment tab switches (UPI vs Cards vs NetBanking)
  const payTabUpi = document.getElementById('payTabUpi');
  const payTabCard = document.getElementById('payTabCard');
  const payTabNet = document.getElementById('payTabNet');
  const payFormUpi = document.getElementById('payFormUpi');
  const payFormCard = document.getElementById('payFormCard');

  if (payTabUpi && payTabCard) {
    payTabUpi.addEventListener('click', () => {
      payTabUpi.classList.add('active');
      payTabCard.classList.remove('active');
      if (payTabNet) payTabNet.classList.remove('active');
      payFormUpi.style.display = 'flex';
      payFormCard.style.display = 'none';
      AppState.booking.payment.method = 'upi';
    });

    payTabCard.addEventListener('click', () => {
      payTabCard.classList.add('active');
      payTabUpi.classList.remove('active');
      if (payTabNet) payTabNet.classList.remove('active');
      payFormUpi.style.display = 'none';
      payFormCard.style.display = 'flex';
      AppState.booking.payment.method = 'card';
    });

    if (payTabNet) {
      payTabNet.addEventListener('click', () => {
        payTabNet.classList.add('active');
        payTabUpi.classList.remove('active');
        payTabCard.classList.remove('active');
        payFormUpi.style.display = 'none';
        payFormCard.style.display = 'flex';
        AppState.booking.payment.method = 'netbanking';
        showToast('Selected NetBanking: HDFC / SBI / ICICI / Axis Bank', 'info');
      });
    }
  }

  // Add-on checkbox change handlers to update subtotal
  document.querySelectorAll('.addon-card input[type="checkbox"]').forEach(chk => {
    chk.addEventListener('change', updateModalTotals);
  });

  // Boarding pass close
  document.getElementById('closeBoardingPassBtn').addEventListener('click', () => {
    document.getElementById('boardingPassOverlay').classList.remove('active');
  });

  // Print Pass button
  document.getElementById('printPassBtn').addEventListener('click', () => {
    window.print();
  });

  // Save trip button
  document.getElementById('saveTripBtn').addEventListener('click', () => {
    showToast('Trip itinerary & DigiYatra pass saved to My Bookings!', 'success');
    document.getElementById('boardingPassOverlay').classList.remove('active');
  });
}

function updateModalStepView() {
  const step = AppState.booking.step;
  
  // Step indicators
  document.querySelectorAll('.step-item').forEach(item => {
    const itemStep = parseInt(item.getAttribute('data-step'));
    item.classList.remove('active', 'completed');
    if (itemStep === step) item.classList.add('active');
    else if (itemStep < step) item.classList.add('completed');
  });

  // Step pages
  document.querySelectorAll('.booking-step-page').forEach((page, idx) => {
    if (idx + 1 === step) page.classList.add('active');
    else page.classList.remove('active');
  });

  // Button labels
  const backBtn = document.getElementById('modalBackBtn');
  const nextBtn = document.getElementById('modalNextBtn');

  backBtn.style.visibility = step === 1 ? 'hidden' : 'visible';

  if (step === 1) {
    nextBtn.querySelector('span').textContent = 'Continue to Seats';
  } else if (step === 2) {
    nextBtn.querySelector('span').textContent = 'Continue to Add-ons';
  } else if (step === 3) {
    nextBtn.querySelector('span').textContent = 'Review & Pay in ₹ (UPI/Card)';
  } else if (step === 4) {
    nextBtn.querySelector('span').textContent = 'Authorize & Issue DigiYatra Pass';
  }

  updateModalTotals();
}

// Generate Fuselage Seat Map
function renderAirplaneCabinSeatMap() {
  const cabin = document.getElementById('cabinBody');
  if (!cabin) return;
  cabin.innerHTML = '';

  const rowsCount = 16;
  const occupiedSeats = ['1A', '1C', '2B', '3F', '4A', '5D', '6B', '7C', '8E', '9A', '10F', '12B', '14E', '15A'];

  for (let r = 1; r <= rowsCount; r++) {
    const isPremium = r <= 3;
    const rowEl = document.createElement('div');
    rowEl.className = 'seat-row';

    // Row number
    const numBadge = document.createElement('span');
    numBadge.className = 'row-num-badge';
    numBadge.textContent = r;
    rowEl.appendChild(numBadge);

    // Left block: A, B, C
    ['A', 'B', 'C'].forEach(seatLetter => {
      const seatCode = `${r}${seatLetter}`;
      const seat = createSeatElement(seatCode, isPremium, occupiedSeats.includes(seatCode));
      rowEl.appendChild(seat);
    });

    // Aisle
    const aisle = document.createElement('div');
    aisle.className = 'seat-aisle-gap';
    rowEl.appendChild(aisle);

    // Right block: D, E, F
    ['D', 'E', 'F'].forEach(seatLetter => {
      const seatCode = `${r}${seatLetter}`;
      const seat = createSeatElement(seatCode, isPremium, occupiedSeats.includes(seatCode));
      rowEl.appendChild(seat);
    });

    cabin.appendChild(rowEl);
  }
}

function createSeatElement(seatCode, isPremium, isOccupied) {
  const seat = document.createElement('button');
  seat.type = 'button';
  seat.className = `airplane-seat ${isPremium ? 'premium' : ''} ${isOccupied ? 'occupied' : ''} ${seatCode === AppState.booking.selectedSeat ? 'selected' : ''}`;
  seat.textContent = seatCode;

  if (isOccupied) {
    seat.setAttribute('disabled', 'true');
    seat.title = `Seat ${seatCode} (Occupied)`;
  } else {
    seat.title = `Seat ${seatCode} ${isPremium ? '(Extra Legroom +₹450)' : '(Included)'}`;
    seat.addEventListener('click', () => {
      document.querySelectorAll('.airplane-seat').forEach(s => s.classList.remove('selected'));
      seat.classList.add('selected');
      AppState.booking.selectedSeat = seatCode;
      AppState.booking.selectedSeatPrice = isPremium ? 450 : 0;

      document.getElementById('selectedSeatNumDisplay').textContent = `Seat ${seatCode}`;
      document.getElementById('selectedSeatPriceDisplay').textContent = isPremium ? '(Extra Legroom +₹450.00)' : '(Free standard seat)';
      updateModalTotals();
    });
  }

  return seat;
}

function updateModalTotals() {
  if (!AppState.selectedFlight) return;

  const base = AppState.selectedFlight.price;
  const seatExtra = AppState.booking.selectedSeatPrice || 0;
  
  let addonsSum = 0;
  if (document.getElementById('addonBaggageCheck')?.checked) addonsSum += 1200;
  if (document.getElementById('addonMealCheck')?.checked) addonsSum += 350;
  if (document.getElementById('addonPriorityCheck')?.checked) addonsSum += 299;
  if (document.getElementById('addonInsuranceCheck')?.checked) addonsSum += 199;
  if (document.getElementById('addonCarbonCheck')?.checked) addonsSum += 49;

  const taxes = 550; // DGCA Passenger Service Fee & Airport Development Fee
  const total = base + seatExtra + addonsSum + taxes;

  document.getElementById('modalFooterTotal').textContent = formatCurrency(total);
}

function populateCheckoutSummary() {
  const flight = AppState.selectedFlight;
  const pax = AppState.booking.paxDetails;
  
  document.getElementById('chkRoute').textContent = `${flight.originCity} (${flight.origin}) ➔ ${flight.destCity} (${flight.destination})`;
  document.getElementById('chkBasePrice').textContent = formatCurrency(flight.price);
  document.getElementById('chkPaxName').textContent = `${pax.firstName} ${pax.lastName}`;
  document.getElementById('chkSeatNum').textContent = `${AppState.booking.selectedSeat} ${AppState.booking.selectedSeatPrice > 0 ? '(+₹450.00)' : '(Included)'}`;

  let addonsTotal = 0;
  if (AppState.booking.addons.baggage) addonsTotal += 1200;
  if (AppState.booking.addons.meal) addonsTotal += 350;
  if (AppState.booking.addons.priority) addonsTotal += 299;
  if (AppState.booking.addons.insurance) addonsTotal += 199;
  if (AppState.booking.addons.carbon) addonsTotal += 49;

  document.getElementById('chkAddonsTotal').textContent = formatCurrency(addonsTotal);
  document.getElementById('chkTaxes').textContent = formatCurrency(550);

  const grandTotal = flight.price + AppState.booking.selectedSeatPrice + addonsTotal + 550;
  document.getElementById('chkGrandTotal').textContent = formatCurrency(grandTotal);
}

// ==========================================
// 6. BOOKING CONFIRMATION & BOARDING PASS
// ==========================================
function completeBooking() {
  const flight = AppState.selectedFlight;
  const pax = AppState.booking.paxDetails;
  const pnr = `${flight.airline.code}-IND${Math.floor(100 + Math.random() * 900)}`;
  const seat = AppState.booking.selectedSeat;
  const gate = `${String.fromCharCode(65 + Math.floor(Math.random() * 4))}${Math.floor(10 + Math.random() * 35)}`;

  // Save itinerary to local storage
  const newTrip = {
    pnr,
    flightNo: flight.id,
    airline: flight.airline.name,
    origin: flight.origin,
    destination: flight.destination,
    originCity: flight.originCity,
    destCity: flight.destCity,
    depTime: flight.depTime,
    arrTime: flight.arrTime,
    date: AppState.search.departDate,
    seat,
    gate,
    paxName: `${pax.lastName.toUpperCase()} / ${pax.firstName.toUpperCase()}`,
    price: flight.price
  };

  AppState.savedTrips.unshift(newTrip);
  localStorage.setItem('flyora_trips', JSON.stringify(AppState.savedTrips));
  updateTripsCountBadge();

  // Sync with Flask SQLite Database for DevOps Persistent Storage
  try {
    fetch('/api/book', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pnr: pnr,
        flight_number: flight.id,
        airline: flight.airline.name,
        origin: flight.origin,
        destination: flight.destination,
        depart_date: AppState.search.departDate,
        depart_time: flight.depTime,
        passenger_name: `${pax.firstName} ${pax.lastName}`,
        email: pax.email,
        phone: pax.phone,
        seat_number: seat,
        cabin_class: AppState.search.cabinClass,
        fare_amount: flight.price,
        currency: AppState.currency.code,
        payment_method: AppState.booking.payment.method.toUpperCase()
      })
    }).catch(() => { /* Local preview fallback */ });
  } catch(e) {}

  // Populate Boarding Pass Modal (DigiYatra Compliant)
  document.getElementById('passAirlineName').textContent = flight.airline.name;
  document.getElementById('passCabinBadge').textContent = `${AppState.search.cabinClass.toUpperCase()} • DIGIYATRA`;
  document.getElementById('passOriginCode').textContent = flight.origin;
  document.getElementById('passOriginName').textContent = flight.originCity;
  document.getElementById('passDestCode').textContent = flight.destination;
  document.getElementById('passDestName').textContent = flight.destCity;
  document.getElementById('passDuration').textContent = flight.duration;
  document.getElementById('passFlightNo').textContent = flight.id;
  document.getElementById('passPaxName').textContent = `${pax.lastName.toUpperCase()} / ${pax.firstName.toUpperCase()} MR`;
  document.getElementById('passFlightCode').textContent = flight.id;
  document.getElementById('passDate').textContent = new Date(AppState.search.departDate).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase();
  document.getElementById('passBoardingTime').textContent = flight.depTime;
  document.getElementById('passGate').textContent = gate;
  document.getElementById('passSeat').textContent = seat;
  document.getElementById('passPnr').textContent = pnr;
  document.getElementById('passBarcodeText').textContent = `M1${pax.lastName.toUpperCase()}/${pax.firstName.toUpperCase()} E-TKT 016789421598 ${flight.origin} ${flight.destination} ${flight.id} ${seat} ${gate} DIGIYATRA`;

  // Stub
  document.getElementById('stubPaxName').textContent = `${pax.lastName.toUpperCase()} / ${pax.firstName.toUpperCase()}`;
  document.getElementById('stubFlightDate').textContent = `${flight.id} • ${newTrip.date}`;
  document.getElementById('stubRoute').textContent = `${flight.origin} ➔ ${flight.destination}`;
  document.getElementById('stubGate').textContent = gate;
  document.getElementById('stubSeat').textContent = seat;

  // Close booking wizard and show boarding pass
  document.getElementById('bookingModalOverlay').classList.remove('active');
  document.getElementById('boardingPassOverlay').classList.add('active');

  showToast('UPI / Payment Authorized! DigiYatra Boarding Pass Issued.', 'success');
}

// ==========================================
// 7. LIVE RADAR / FLIGHT TRACKER (INDIA)
// ==========================================
function initFlightTracker() {
  const trackBtn = document.getElementById('trackFlightBtn');
  const input = document.getElementById('flightTrackerInput');

  trackBtn.addEventListener('click', () => {
    const query = input.value.trim().toUpperCase();
    if (!query) return;

    // Simulated lookup for Indian flights
    const planeIcon = document.getElementById('trackerPlaneIcon');
    const progressBar = document.getElementById('trackerProgressBar');
    const pct = Math.floor(40 + Math.random() * 45);

    planeIcon.style.left = `${pct}%`;
    progressBar.style.width = `${pct}%`;

    const airlineName = query.startsWith('6E') ? 'IndiGo' : (query.startsWith('AI') ? 'Air India' : (query.startsWith('UK') ? 'Vistara' : (query.startsWith('QP') ? 'Akasa Air' : 'Flyora Partner')));

    document.getElementById('trackerFlightCode').textContent = `${query} • ${airlineName} Live Radar`;
    document.getElementById('trackerAltitude').textContent = `${(32000 + Math.floor(Math.random() * 6000)).toLocaleString()} ft`;
    document.getElementById('trackerSpeed').textContent = `${440 + Math.floor(Math.random() * 40)} kts`;
    document.getElementById('trackerRemaining').textContent = `${Math.floor(0 + Math.random() * 2)}h ${Math.floor(15 + Math.random() * 40)}m`;

    showToast(`Live radar telemetry updated for ${query} (${airlineName})`, 'success');
  });
}

// ==========================================
// 8. POPULAR INDIAN DESTINATIONS
// ==========================================
function initDestinations() {
  const tabs = document.querySelectorAll('.dest-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const cat = tab.getAttribute('data-category');
      renderDestinations(cat);
    });
  });
}

function renderDestinations(category = 'all') {
  const grid = document.getElementById('destinationsGrid');
  if (!grid) return;
  grid.innerHTML = '';

  const list = category === 'all' ? DESTINATIONS_DATA : DESTINATIONS_DATA.filter(d => d.category === category);

  list.forEach(dest => {
    const card = document.createElement('div');
    card.className = 'dest-card';
    card.innerHTML = `
      <div class="dest-card-bg" style="background-image: url('${dest.image}');"></div>
      <div class="dest-card-overlay">
        <div class="dest-tag-row">
          <span class="dest-cat-badge">${dest.country}</span>
          <span class="dest-weather-pill"><i data-lucide="cloud-sun"></i> ${dest.weather}</span>
        </div>
        <div class="dest-card-info">
          <h3 class="dest-city-title">${dest.city}</h3>
          <span class="dest-country-name">${dest.country} (${dest.iata})</span>
          <div class="dest-price-action-row">
            <div>
              <span class="dest-fare-from">Direct Fares from</span>
              <div class="dest-fare-val">${formatCurrency(dest.price)}</div>
            </div>
            <button class="dest-book-btn">Book Flight ➔</button>
          </div>
        </div>
      </div>
    `;

    card.addEventListener('click', () => {
      const airport = AIRPORTS.find(a => a.code === dest.iata) || { code: dest.iata, city: dest.city, name: dest.city, country: 'India' };
      AppState.search.destination = airport;
      document.getElementById('destInput').value = `${airport.city} (${airport.code})`;
      document.getElementById('destCodeBadge').textContent = airport.code;

      generateMockFlights();
      scrollToResults();
      showToast(`Selected destination: ${dest.city} (${dest.iata})`, 'info');
    });

    grid.appendChild(card);
  });

  if (window.lucide) lucide.createIcons();
}

// ==========================================
// 9. FLYORA AI COPILOT CHAT ENGINE (INDIA FOCUS)
// ==========================================
function initAiCopilot() {
  const overlay = document.getElementById('aiDrawerOverlay');
  const trigger1 = document.getElementById('aiCopilotBtn');
  const trigger2 = document.getElementById('openAiDrawerBtn');
  const trigger3 = document.getElementById('footerAiLink');
  const closeBtn = document.getElementById('closeAiDrawerBtn');
  const form = document.getElementById('aiChatForm');
  const input = document.getElementById('aiChatInput');

  const openDrawer = (e) => {
    if (e) e.preventDefault();
    overlay.classList.add('active');
  };

  if (trigger1) trigger1.addEventListener('click', openDrawer);
  if (trigger2) trigger2.addEventListener('click', openDrawer);
  if (trigger3) trigger3.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', () => overlay.classList.remove('active'));

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const txt = input.value.trim();
    if (!txt) return;

    appendChatMessage('user', txt);
    input.value = '';

    // Generate intelligent Indian AI response
    setTimeout(() => {
      generateAiResponse(txt);
    }, 500);
  });

  // Chip triggers
  document.querySelectorAll('.ai-prompt-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const prompt = chip.getAttribute('data-prompt');
      appendChatMessage('user', prompt);
      setTimeout(() => generateAiResponse(prompt), 500);
    });
  });
}

function appendChatMessage(role, text) {
  const container = document.getElementById('aiChatBody');
  const msg = document.createElement('div');
  msg.className = `ai-msg ${role}`;

  if (role === 'bot') {
    msg.innerHTML = `
      <div class="ai-avatar-mini"><i data-lucide="bot"></i></div>
      <div class="msg-bubble">${text}</div>
    `;
  } else {
    msg.innerHTML = `
      <div class="msg-bubble">${escapeHtml(text)}</div>
    `;
  }

  container.appendChild(msg);
  container.scrollTop = container.scrollHeight;
  if (window.lucide) lucide.createIcons();
}

function generateAiResponse(query) {
  const q = query.toLowerCase();
  let reply = '';

  if (q.includes('goa') || q.includes('beach')) {
    reply = `🏖️ <strong>Goa Getaway Intelligence:</strong><br>
    • <strong>Best Rates:</strong> Non-stop flights from Delhi (DEL) & Mumbai (BOM) to Goa (GOI/GOX) start from <strong>₹2,899 - ₹3,499</strong> on Tuesdays & Wednesdays.<br>
    • <strong>Airport Tip:</strong> Choose Mopa (GOX) for North Goa (Vagator, Morjim) and Dabolim (GOI) for South Goa (Colva, Palolem).<br>
    • <strong>Best Season:</strong> Mid-October to March for sunny beach weather.`;
  } else if (q.includes('kashmir') || q.includes('srinagar') || q.includes('ladakh') || q.includes('snow')) {
    reply = `🏔️ <strong>Kashmir & Ladakh Travel Advice:</strong><br>
    • <strong>Srinagar (SXR):</strong> Direct flights from Delhi start at <strong>₹4,499</strong>. Best months for snowfall are Dec-Feb, and tulip bloom in April.<br>
    • <strong>Leh Ladakh (IXL):</strong> Early morning flights from Delhi from <strong>₹5,999</strong>. Note: Kushok Bakula Airport has high altitude; take 24h rest upon arrival.`;
  } else if (q.includes('baggage') || q.includes('luggage') || q.includes('dgca') || q.includes('rules')) {
    reply = `🧳 <strong>DGCA Domestic Baggage Rules (India):</strong><br>
    • <strong>Check-in Baggage:</strong> 15kg per passenger is free on IndiGo, Air India, Vistara, Akasa Air & SpiceJet (Air India offers up to 25kg on select tickets).<br>
    • <strong>Cabin Bag:</strong> 1 piece up to 7kg + 1 small laptop bag/purse.<br>
    • <strong>Student Benefit:</strong> Select the 'Student' special fare pill to get <strong>10kg extra check-in baggage</strong> for free!`;
  } else if (q.includes('varanasi') || q.includes('spiritual') || q.includes('ayodhya') || q.includes('temple')) {
    reply = `🕉️ <strong>Spiritual Circuit Planner:</strong><br>
    • <strong>Varanasi (VNS):</strong> Direct flights from Delhi & Mumbai from <strong>₹2,999</strong>. Perfect for Ganga Aarti and Sarnath tours.<br>
    • <strong>Ayodhya (AYJ):</strong> Daily direct flights via IndiGo & Air India Express from <strong>₹3,199</strong>.<br>
    • <strong>Tirupati (TIR):</strong> Direct flights from Hyderabad & Bengaluru from <strong>₹2,699</strong>.`;
  } else if (q.includes('kerala') || q.includes('kochi') || q.includes('munnar')) {
    reply = `🌴 <strong>Kerala Backwaters Tour:</strong><br>
    • Flights from Delhi, Mumbai & Bengaluru to Kochi (COK) start at <strong>₹3,899</strong>.<br>
    • <strong>Suggested 5-Day Circuit:</strong> Kochi (Heritage Fort Kochi) ➔ Munnar (Tea plantations) ➔ Alleppey (Houseboat stay) ➔ Kochi departure.`;
  } else {
    reply = `✈️ <strong>Flyora Indian Skies Travel AI:</strong><br>
    Based on 50M+ domestic flight booking transactions across India, flights departing on <strong>Tuesdays and Wednesdays</strong> are on average <strong>15.4% cheaper</strong> than weekend flights.<br>
    Book with instant UPI on Flyora with ₹0 gateway convenience charges! Let me know your preferred departure city and travel dates.`;
  }

  appendChatMessage('bot', reply);
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// ==========================================
// 10. MY TRIPS DRAWER & PERSISTENCE
// ==========================================
function initMyTrips() {
  const overlay = document.getElementById('tripsDrawerOverlay');
  const openBtn = document.getElementById('myTripsBtn');
  const closeBtn = document.getElementById('closeTripsDrawerBtn');

  openBtn.addEventListener('click', () => {
    renderSavedTrips();
    overlay.classList.add('active');
  });

  closeBtn.addEventListener('click', () => overlay.classList.remove('active'));
}

function renderSavedTrips() {
  const container = document.getElementById('savedTripsContainer');
  const subCount = document.getElementById('tripsDrawerCountSub');
  if (!container) return;
  container.innerHTML = '';

  const trips = AppState.savedTrips;
  subCount.textContent = `${trips.length} Active Itinerar${trips.length === 1 ? 'y' : 'ies'}`;

  if (trips.length === 0) {
    container.innerHTML = `
      <div class="empty-trips-view">
        <i data-lucide="ticket"></i>
        <h4>No Booked Trips Found</h4>
        <p>Your confirmed Indian flight tickets & DigiYatra boarding passes will appear here.</p>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
    return;
  }

  trips.forEach((trip, idx) => {
    const item = document.createElement('div');
    item.className = 'saved-trip-item glass-panel';
    item.innerHTML = `
      <div class="trip-item-header">
        <span class="trip-pnr-pill">PNR: ${trip.pnr}</span>
        <span class="pulse-dot"></span>
      </div>
      <div class="trip-route-title">${trip.origin} ➔ ${trip.destination}</div>
      <div class="trip-meta-row">
        <span>${trip.flightNo} • ${trip.airline}</span>
        <span>Seat: <strong>${trip.seat}</strong> (Gate ${trip.gate})</span>
      </div>
      <div class="trip-meta-row">
        <span>Date: ${trip.date}</span>
        <span>Passenger: ${trip.paxName}</span>
      </div>
      <div class="trip-actions-row">
        <button class="btn btn-secondary btn-sm print-saved-pass-btn" data-idx="${idx}">
          <i data-lucide="printer"></i> View DigiYatra Pass
        </button>
        <button class="btn btn-glass btn-sm cancel-trip-btn" data-idx="${idx}" style="color: var(--brand-rose);">
          Cancel
        </button>
      </div>
    `;

    // View Pass
    item.querySelector('.print-saved-pass-btn').addEventListener('click', () => {
      document.getElementById('tripsDrawerOverlay').classList.remove('active');
      
      // Repopulate pass
      document.getElementById('passAirlineName').textContent = trip.airline;
      document.getElementById('passOriginCode').textContent = trip.origin;
      document.getElementById('passOriginName').textContent = trip.originCity;
      document.getElementById('passDestCode').textContent = trip.destination;
      document.getElementById('passDestName').textContent = trip.destCity;
      document.getElementById('passFlightNo').textContent = trip.flightNo;
      document.getElementById('passPaxName').textContent = trip.paxName;
      document.getElementById('passFlightCode').textContent = trip.flightNo;
      document.getElementById('passDate').textContent = trip.date;
      document.getElementById('passBoardingTime').textContent = trip.depTime;
      document.getElementById('passGate').textContent = trip.gate;
      document.getElementById('passSeat').textContent = trip.seat;
      document.getElementById('passPnr').textContent = trip.pnr;
      
      document.getElementById('boardingPassOverlay').classList.add('active');
    });

    // Cancel Trip
    item.querySelector('.cancel-trip-btn').addEventListener('click', () => {
      AppState.savedTrips.splice(idx, 1);
      localStorage.setItem('flyora_trips', JSON.stringify(AppState.savedTrips));
      renderSavedTrips();
      updateTripsCountBadge();
      showToast(`Booking ${trip.pnr} cancelled. Instant UPI refund initiated.`, 'info');
    });

    container.appendChild(item);
  });

  if (window.lucide) lucide.createIcons();
}

function updateTripsCountBadge() {
  const badge = document.getElementById('tripsCountBadge');
  if (badge) {
    badge.textContent = AppState.savedTrips.length;
  }
}

// ==========================================
// 11. NEWSLETTER & TOAST ENGINE
// ==========================================
function initNewsletter() {
  const form = document.getElementById('newsletterForm');
  const input = document.getElementById('nlEmailInput');

  form.addEventListener('submit', () => {
    const email = input.value.trim();
    if (email) {
      showToast(`🎉 ₹500 Flight Voucher Code "FLYINDIA500" sent to ${email}`, 'success');
      input.value = '';
    }
  });
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  const iconName = type === 'success' ? 'check-circle-2' : (type === 'error' ? 'alert-triangle' : 'info');
  toast.innerHTML = `<i data-lucide="${iconName}"></i> <span>${message}</span>`;
  
  container.appendChild(toast);
  if (window.lucide) lucide.createIcons();

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
