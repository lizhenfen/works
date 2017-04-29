import views
from apis import index

uri = [
            (r'/', views.IndexHandler),
            (r'/test', views.TestHandler),
            (r'/login', views.LoginHandler),
            (r'/logout', views.LogoutHandler),
            (r'/company/count', views.GroupByCompanyHandler),
            (r'/company/visit/count', views.AnalyzeByCompanyVisitHandler),
            (r'/employee/count', views.GroupByEmployeeHandler),
            (r'/employee/visit/count', views.AnalyzeByPersonVisitHandler),
            (r'/echart/(\w+)', views.EchartsHandler),
            (r'/echarts/api/company', views.ApiCompanyTrendHandler),
            (r'/echarts/api/person', views.ApiPersonTrendHandler),
            (r'/search', views.ApiAutoCompleteHandler),
            (r'/nginx', views.NginxConfigHandler),
            (r'/api/person/trend', views.LoadPersonOnGpost),
            #(r'/api/oraclde/sum', views.OracleQueryHandler)
            # index apis
            (r'/apis/index/ccount', index.APIIndexClassCountByCustom),
            (r'/apis/index/countall', index.APIIndexAllCount),
        ]