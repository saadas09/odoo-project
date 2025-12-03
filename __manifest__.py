# -*- coding: utf-8 -*-
{
    'name': 'Hotel Reservation System',
    'version': '16.0.1.0.0',
    'category': 'Hospitality',
    'summary': 'Complete hotel reservation management with API synchronization',
    'description': """
        Hotel Reservation System
        =========================
        * Manage hotel rooms
        * Manage clients
        * Manage reservations
        * Automatic price calculation
        * Prevent overlapping reservations
        * Synchronization with Booking.com and Airbnb via API
        * Web interface for customer reservations
        * CRON tasks for synchronization
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'portal',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/scheduled_jobs.xml',
        'views/room_views.xml',
        'views/reservation_views.xml',
        'views/client_views.xml',
        'views/menus.xml',
        'views/portal_templates.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
