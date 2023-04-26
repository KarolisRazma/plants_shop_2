# WorkplaceWebService

Workplaces and Positions web service for university assignment

# Instructions

1. git clone https://github.com/AleksandrasJ/WorkplaceWebService.git
2. cd WorkplaceWebService
3. docker-compose up -d

# Requests

## GET

URL: http://localhost:80/workplaces<br />
URL: http://localhost:80/workplaces/1<br />
URL: http://localhost:80/workplaces/1/positions<br />
URL: http://localhost:80/workplaces/1/positions/1<br />
URL: http://localhost:80/positions<br />
URL: http://localhost:80/positions/1<br />

## POST

URL: http://localhost:80/workplaces<br />
BODY: 
```
{
    "companyName": "IBM",
    "description": "At IBM, we do more than work. We create. We create as technologists, developers, and engineers. We create with our partners. We create with our competitors. If you're searching for ways to make the world work better through technology and infrastructure, software and consulting, then we want to work with you.",
    "industry": "IT Services and IT Consulting",
    "website": "http://www.ibm.com",
    "specialities": [
        "Cloud",
        "Security"
    ]
}
```
URL: http://localhost:80/workplaces/1/positions<br />
BODY: 
```
{
    "positionName": "Java Developer",
    "location": "Vilnius",
    "workTimeNorm": "Full-time",
    "description": "IBM CIC Baltic Custom Development department is looking for a Full Stack developer. In this role, you will use the latest tools and technologies available to deliver state-of-the-art software. You'll be responsible for ensuring that software components are expertly designed, tested, debugged, verified, and ready for integration into IBM's best-of-breed solutions that help our clients improve their business outcomes in the global marketplace",
    "requirements": [
        "Solid work experience with Java 8 or higher",
        "Hands-on experience with SQL",
        "Hands-on experience with GitHub",
        "Feeling comfortable in Agile / DevOps environment"
    ],
    "salary": 3600
}
```
## PUT

URL: http://localhost:80/workplaces/1<br />
BODY: 
```
{
    "companyName": "IBM",
    "description": "At IBM, we do more than work. We create. We create as technologists, developers, and engineers. We create with our partners. We create with our competitors. If you're searching for ways to make the world work better through technology and infrastructure, software and consulting, then we want to work with you.",
    "industry": "IT Services and IT Consulting",
    "website": "http://www.ibm.com",
    "specialities": [
        "Cloud",
        "Security",
        "Systems services",
        "Resiliency services",
        "Internet of Things"
    ]
}
```
URL: http://localhost:80/workplaces/1/positions/1<br />
BODY: 
```
{
    "positionName": "Java Developer",
    "location": "Vilnius",
    "workTimeNorm": "Full-time",
    "description": "IBM CIC Baltic Custom Development department is looking for a Full Stack developer. In this role, you will use the latest tools and technologies available to deliver state-of-the-art software. You'll be responsible for ensuring that software components are expertly designed, tested, debugged, verified, and ready for integration into IBM's best-of-breed solutions that help our clients improve their business outcomes in the global marketplace",
    "requirements": [
        "Solid work experience with Java 8 or higher",
        "Hands-on experience with SQL",
        "Hands-on experience with GitHub",
        "Feeling comfortable in Agile / DevOps environment"
    ],
    "salary": 4300
}
```
URL: http://localhost:80/positions/1
```
{
    "positionName": "Java Developer",
    "location": "Vilnius",
    "workTimeNorm": "Full-time",
    "description": "IBM CIC Baltic Custom Development department is looking for a Full Stack developer. In this role, you will use the latest tools and technologies available to deliver state-of-the-art software. You'll be responsible for ensuring that software components are expertly designed, tested, debugged, verified, and ready for integration into IBM's best-of-breed solutions that help our clients improve their business outcomes in the global marketplace",
    "requirements": [
        "Solid work experience with Java 8 or higher",
        "Hands-on experience with SQL",
        "Hands-on experience with GitHub",
        "Feeling comfortable in Agile / DevOps environment"
    ],
    "salary": 4300
}
```

## DELETE

URL: http://localhost:80/workplaces/1<br />
URL: http://localhost:80/workplaces/1/positions/1<br />
URL: http://localhost:80/positions/1<br />
