"""
Ensures the data/ directory and seed JSON files exist at startup.
Safe to call on every boot — only writes if a file is missing.
"""
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

SEED = {
    'invoices.json': {
        '9876543210': [
            {
                'invoice_id': 'INV-20261101',
                'billing_period': '01 May 2026 – 30 May 2026',
                'due_date': '2026-06-04',
                'total_amount': 1249,
                'status': 'unpaid',
                'line_items': [
                    {'description': 'Monthly plan — ₹699 postpaid', 'amount': 699, 'type': 'plan_charge'},
                    {'description': 'SAARC roaming pack — 14 days', 'amount': 299, 'type': 'addon_charge', 'activated_on': '2026-05-14'},
                    {
                        'description': 'Excess data — 8.4 GB beyond daily limit',
                        'amount': 251,
                        'type': 'excess_usage',
                        'usage_dates': ['2024-11-11', '2024-11-12']
                    }
                ]
            }
        ],
        '7406179387': [
            {
                'invoice_id': 'INV-20261101',
                'billing_period': '01 May 2026 – 30 May 2026',
                'due_date': '2026-06-04',
                'total_amount': 1249,
                'status': 'unpaid',
                'line_items': [
                    {'description': 'Monthly plan — ₹699 postpaid', 'amount': 699, 'type': 'plan_charge'},
                    {'description': 'SAARC roaming pack — 14 days', 'amount': 299, 'type': 'addon_charge', 'activated_on': '2026-05-14'},
                    {
                        'description': 'Excess data — 8.4 GB beyond daily limit',
                        'amount': 251,
                        'type': 'excess_usage',
                        'usage_dates': ['2024-11-11', '2024-11-12']
                    }
                ]
            }
        ],
        '9858509904': [
            {
                'invoice_id': 'INV-20261101',
                'billing_period': '01 May 2026 – 30 May 2026',
                'due_date': '2026-06-04',
                'total_amount': 699,
                'status': 'unpaid',
                'line_items': [
                    {'description': 'Monthly plan — ₹499 postpaid', 'amount': 499, 'type': 'plan_charge'}
                ]
            }
        ]
    },
    'activation_log.json': {
        '9876543210': [
            {
                'event_id': 'ACT-99201',
                'service_name': 'SAARC Roaming Pack',
                'status': 'active',
                'activated_on': '2026-05-14',
                'validity': '14 days',
                'charge': 299,
                'channel': 'system_auto'
            },
            {
                'event_id': 'ACT-9890',
                'service_name': 'Monthly plan — ₹699',
                'status': 'renewed',
                'activated_on': '2026-05-01',
                'validity': '30 days',
                'charge': 699,
                'channel': 'self_service_app'
            }
        ],
        '7406179387': [
            {
                'event_id': 'ACT-99201',
                'service_name': 'SAARC Roaming Pack',
                'status': 'active',
                'activated_on': '2026-05-14',
                'validity': '14 days',
                'charge': 299,
                'channel': 'system_auto'
            },
            {
                'event_id': 'ACT-9890',
                'service_name': 'Monthly plan — ₹699',
                'status': 'renewed',
                'activated_on': '2026-05-01',
                'validity': '30 days',
                'charge': 699,
                'channel': 'self_service_app'
            }
        ],
        '9858509904': [
            {
                'event_id': 'ACT-9890',
                'service_name': 'Monthly plan — ₹499',
                'status': 'renewed',
                'activated_on': '2026-05-01',
                'validity': '30 days',
                'charge': 499,
                'channel': 'self_service_app'
            }
        ]
    },
    'account_balance.json': {
        '7406179387': {'current_balance': 1249.0, 'currency': 'INR', 'last_payment': {'amount': 699, 'date': '2026-04-04', 'method': 'UPI'}, 'next_due_date': '2026-06-04', 'plan_name': '₹699 Postpaid Premium'},
        '9858509904': {'current_balance': 849.0, 'currency': 'INR', 'last_payment': {'amount': 499, 'date': '2026-04-04', 'method': 'UPI'}, 'next_due_date': '2026-06-04', 'plan_name': '₹499 Postpaid'},
        '9876543210': {'current_balance': 1249.0, 'currency': 'INR', 'last_payment': {'amount': 699, 'date': '2026-04-04', 'method': 'UPI'}, 'next_due_date': '2026-06-04', 'plan_name': '₹699 Postpaid Premium'}
    },
    'usage_history.json': {
        '7406179387': [
            {'date': '2026-05-11', 'data_used_gb': 12.5, 'daily_limit_gb': 4.0, 'excess_gb': 8.5, 'calls_minutes': 65, 'sms_count': 4},
            {'date': '2026-05-12', 'data_used_gb': 10.2, 'daily_limit_gb': 4.0, 'excess_gb': 6.2, 'calls_minutes': 55, 'sms_count': 2},
            {'date': '2026-05-13', 'data_used_gb': 8.5, 'daily_limit_gb': 4.0, 'excess_gb': 4.5, 'calls_minutes': 48, 'sms_count': 0},
            {'date': '2026-05-14', 'data_used_gb': 9.2, 'daily_limit_gb': 4.0, 'excess_gb': 5.2, 'calls_minutes': 72, 'sms_count': 5},
            {'date': '2026-05-15', 'data_used_gb': 11.8, 'daily_limit_gb': 4.0, 'excess_gb': 7.8, 'calls_minutes': 60, 'sms_count': 3},
            {'date': '2026-05-01', 'data_used_gb': 4.5, 'daily_limit_gb': 4.0, 'excess_gb': 0.5, 'calls_minutes': 45, 'sms_count': 2}
        ],
        '9858509904': [
            {'date': '2026-05-11', 'data_used_gb': 2.4, 'daily_limit_gb': 2.5, 'excess_gb': 0, 'calls_minutes': 35, 'sms_count': 1},
            {'date': '2026-05-12', 'data_used_gb': 2.3, 'daily_limit_gb': 2.5, 'excess_gb': 0, 'calls_minutes': 40, 'sms_count': 0},
            {'date': '2026-05-13', 'data_used_gb': 2.6, 'daily_limit_gb': 2.5, 'excess_gb': 0.1, 'calls_minutes': 28, 'sms_count': 2},
            {'date': '2026-05-14', 'data_used_gb': 2.2, 'daily_limit_gb': 2.5, 'excess_gb': 0, 'calls_minutes': 32, 'sms_count': 1},
            {'date': '2026-05-15', 'data_used_gb': 2.5, 'daily_limit_gb': 2.5, 'excess_gb': 0, 'calls_minutes': 45, 'sms_count': 3}
        ],
        '9876543210': [
            {'date': '2026-05-11', 'data_used_gb': 1.2, 'daily_limit_gb': 4.0, 'excess_gb': 0, 'calls_minutes': 15, 'sms_count': 0},
            {'date': '2026-05-12', 'data_used_gb': 1.4, 'daily_limit_gb': 4.0, 'excess_gb': 0, 'calls_minutes': 20, 'sms_count': 1},
            {'date': '2026-05-13', 'data_used_gb': 0.9, 'daily_limit_gb': 4.0, 'excess_gb': 0, 'calls_minutes': 10, 'sms_count': 0},
            {'date': '2026-05-14', 'data_used_gb': 1.1, 'daily_limit_gb': 4.0, 'excess_gb': 0, 'calls_minutes': 25, 'sms_count': 2},
            {'date': '2026-05-15', 'data_used_gb': 1.3, 'daily_limit_gb': 4.0, 'excess_gb': 0, 'calls_minutes': 18, 'sms_count': 0}
        ]
    },
    'tickets.json': [
        {
            'ticket_id': 'BTC-88101',
            'created_at': '2026-05-14T10:30:00Z',
            'mobile_number': '9876543210',
            'type': 'billing_dispute',
            'issue_summary': 'Excess data charge inquiry for May 12.',
            'root_cause': 'customer_unaware_of_usage',
            'action_taken': 'Explained 5G usage consumption. Customer satisfied.',
            'credit_amount': 0.0,
            'credit_id': None,
            'priority': 'low',
            'resolution_status': 'resolved',
            'raised_by': 'aarav_billing_agent'
        }
    ],
    'current_plan.json': {
        '7406179387': {
            "customer_name": "Purusottam Singh",
            "plan_id": "PLN-POSTPAID-699",
            "plan_name": "Rs 699 Postpaid Premium",
            "plan_type": "postpaid",
            "price_rs": 699,
            "data_per_month_gb": 125,
            "calls": "Unlimited to all networks",
            "sms_per_month": 100,
            "billing_date": 4,
            "circle": "Karnataka",
            "5g_enabled": True,
            "international_roaming": False
        },
        '9858509904': {
            "customer_name": "Madhukar Rao",
            "plan_id": "PLN-POSTPAID-499",
            "plan_name": "Rs 499 Postpaid",
            "plan_type": "postpaid",
            "price_rs": 499,
            "data_per_month_gb": 75,
            "calls": "Unlimited to all networks",
            "sms_per_month": 100,
            "billing_date": 4,
            "circle": "Delhi",
            "5g_enabled": True,
            "international_roaming": False
        },
        '9876543210': {
            "customer_name": "Kavitha Nair",
            "plan_id": "PLN-POSTPAID-699",
            "plan_name": "Rs 699 Postpaid Premium",
            "plan_type": "postpaid",
            "price_rs": 699,
            "data_per_month_gb": 125,
            "calls": "Unlimited to all networks",
            "sms_per_month": 100,
            "billing_date": 4,
            "circle": "Maharashtra",
            "5g_enabled": True,
            "international_roaming": False
        }
    },
    'recharge_history.json': {
        '9876543210': [
            {"month": "May 2026", "base_recharge_rs": 699, "base_plan": "Rs 699 Postpaid Premium", "excess_charges_rs": 0, "total_spend_rs": 699, "next_recharge_due": "2026-06-04", "recharge_consistency": "regular", "total_top_up_spend_rs": 0},
            {"month": "April 2026", "base_recharge_rs": 699, "base_plan": "Rs 699 Postpaid Premium", "excess_charges_rs": 0, "total_spend_rs": 699, "next_recharge_due": "2026-06-04", "recharge_consistency": "regular", "total_top_up_spend_rs": 0}
        ],
        '7406179387': [
            {"month": "May 2026", "base_recharge_rs": 699, "base_plan": "Rs 699 Postpaid Premium", "excess_charges_rs": 550, "total_spend_rs": 1249, "next_recharge_due": "2026-06-04", "recharge_consistency": "regular", "total_top_up_spend_rs": 550},
            {"month": "April 2026", "base_recharge_rs": 699, "base_plan": "Rs 699 Postpaid Premium", "excess_charges_rs": 480, "total_spend_rs": 1179, "next_recharge_due": "2026-06-04", "recharge_consistency": "regular", "total_top_up_spend_rs": 480},
            {"month": "March 2026", "base_recharge_rs": 699, "base_plan": "Rs 699 Postpaid Premium", "excess_charges_rs": 420, "total_spend_rs": 1119, "next_recharge_due": "2026-06-04", "recharge_consistency": "regular", "total_top_up_spend_rs": 420}
        ],
        '9858509904': [
            {"month": "May 2026", "base_recharge_rs": 499, "base_plan": "Rs 499 Postpaid", "excess_charges_rs": 0, "total_spend_rs": 499, "next_recharge_due": "2026-06-04", "recharge_consistency": "regular", "total_top_up_spend_rs": 0}
        ]
    },
    'available_plans.json': [
        {"plan_id": "PLN-POSTPAID-499", "plan_name": "Rs 499 Postpaid", "plan_type": "postpaid", "price_rs": 499, "data_per_month_gb": 75, "calls": "Unlimited to all networks", "sms_per_month": 100, "5g_enabled": True, "international_roaming": False, "extras": [], "circle": "Maharashtra"},
        {"plan_id": "PLN-POSTPAID-499", "plan_name": "Rs 499 Postpaid", "plan_type": "postpaid", "price_rs": 499, "data_per_month_gb": 75, "calls": "Unlimited to all networks", "sms_per_month": 100, "5g_enabled": True, "international_roaming": False, "extras": [], "circle": "Karnataka"},
        {"plan_id": "PLN-POSTPAID-499", "plan_name": "Rs 499 Postpaid", "plan_type": "postpaid", "price_rs": 499, "data_per_month_gb": 75, "calls": "Unlimited to all networks", "sms_per_month": 100, "5g_enabled": True, "international_roaming": False, "extras": [], "circle": "Delhi"},
        {"plan_id": "PLN-POSTPAID-699", "plan_name": "Rs 699 Postpaid Premium", "plan_type": "postpaid", "price_rs": 699, "data_per_month_gb": 125, "calls": "Unlimited to all networks", "sms_per_month": 100, "5g_enabled": True, "international_roaming": False, "extras": ["Bharti Connect TV", "1 OTT subscription"], "circle": "Maharashtra"},
        {"plan_id": "PLN-POSTPAID-699", "plan_name": "Rs 699 Postpaid Premium", "plan_type": "postpaid", "price_rs": 699, "data_per_month_gb": 125, "calls": "Unlimited to all networks", "sms_per_month": 100, "5g_enabled": True, "international_roaming": False, "extras": ["Bharti Connect TV", "1 OTT subscription"], "circle": "Karnataka"},
        {"plan_id": "PLN-POSTPAID-699", "plan_name": "Rs 699 Postpaid Premium", "plan_type": "postpaid", "price_rs": 699, "data_per_month_gb": 125, "calls": "Unlimited to all networks", "sms_per_month": 100, "5g_enabled": True, "international_roaming": False, "extras": ["Bharti Connect TV", "1 OTT subscription"], "circle": "Delhi"},
        {"plan_id": "PLN-POSTPAID-999", "plan_name": "Rs 999 Postpaid Max", "plan_type": "postpaid", "price_rs": 999, "data_per_month_gb": 300, "calls": "Unlimited to all networks + 100 min international to 10 countries", "sms_per_month": 100, "5g_enabled": True, "international_roaming": True, "extras": ["Bharti Connect TV", "2 OTT subscriptions", "Amazon Prime"], "circle": "Maharashtra"},
        {"plan_id": "PLN-POSTPAID-999", "plan_name": "Rs 999 Postpaid Max", "plan_type": "postpaid", "price_rs": 999, "data_per_month_gb": 300, "calls": "Unlimited to all networks + 100 min international to 10 countries", "sms_per_month": 100, "5g_enabled": True, "international_roaming": True, "extras": ["Bharti Connect TV", "2 OTT subscriptions", "Amazon Prime"], "circle": "Karnataka"},
        {"plan_id": "PLN-POSTPAID-999", "plan_name": "Rs 999 Postpaid Max", "plan_type": "postpaid", "price_rs": 999, "data_per_month_gb": 300, "calls": "Unlimited to all networks + 100 min international to 10 countries", "sms_per_month": 100, "5g_enabled": True, "international_roaming": True, "extras": ["Bharti Connect TV", "2 OTT subscriptions", "Amazon Prime"], "circle": "Delhi"}
    ],
    'account_notes.json': {},
    'plan_changes.json': []
}

def ensure_seed_data(force=False):
    os.makedirs(DATA_DIR, exist_ok=True)
    for filename, default in SEED.items():
        path = os.path.join(DATA_DIR, filename)
        if force or not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=2, ensure_ascii=False)
