import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import plotly.express as px
import json

schema = 'warehouse'
layout = go.Layout(plot_bgcolor="#f3f3f3",
                    paper_bgcolor="#f3f3f3",
                    font=dict(family="Roboto Slab, serif",
                                size=14, color="black"),
                   autosize=True,
                   margin=dict(t=50, b=50, l=50, r=50))
colors = px.colors.sequential.Viridis
cmap = 'viridis_r'

def filter_df(df, technology=0, experience=0, work_format=None):
    filtered_gf = df.copy()
    if technology:
        filtered_gf = filtered_gf[filtered_gf['technology']==technology]
    if experience:
        filtered_gf = filtered_gf[filtered_gf['experience']==experience]
    if work_format:
        filtered_gf = filtered_gf[filtered_gf['work_type']==work_format]
    return filtered_gf


def create_time_chart(df, technology=0, experience=0, work_format=None):
    df = filter_df(df, technology, experience, work_format)
    if len(df) > 1:
        timeline = df.groupby('creation_date').agg({'description': 'count'})
        timeline.sort_index(inplace=True)
        timeline = timeline.rename(columns={'description': 'vacancies'})
        timeline = timeline.resample('D').sum()

        data = go.Scatter(
            x=timeline.index,
            y=timeline["vacancies"],
            mode="lines+markers",
            marker=dict(color=colors[2]))

        graph = {"data": [data], "layout": layout}
        return json.dumps(graph, cls=PlotlyJSONEncoder)
    else:
        return None


def create_work_format_chart(df, technology=None):
    df = filter_df(df, technology=technology)
    if len(df)>0:
        by_work_forms = df.groupby('work_type').agg({'description': 'count'})
        by_work_forms = by_work_forms.rename(columns={'description': 'vacancies'})

        data = go.Pie(
            labels=by_work_forms.index,
            values=by_work_forms["vacancies"],
            marker=dict(colors=[colors[1], colors[len(colors)//2], colors[-1]]))

        graph = {"data": [data], "layout": layout}
        return json.dumps(graph, cls=PlotlyJSONEncoder)
    else:
        return None


def create_technologies_chart(df, technologies, experience=None):
    df = filter_df(df, experience=experience)
    if len(df) > 0:
        #technologies = read_table(schema, 'technology', index='id')
        by_technology = df.groupby('technology').agg({'description': 'count'})
        by_technology = by_technology.rename(columns={'description': 'vacancies'})

        index_to_technology = dict(zip(technologies.index, technologies['technology']))
        by_technology.index = by_technology.index.map(index_to_technology)
        by_technology.sort_index(inplace=True)

        data = go.Bar(
                x=by_technology.index,
                y=by_technology["vacancies"],
                marker=dict(color=by_technology["vacancies"], colorscale=cmap))

        graph = {"data": [data], "layout": layout}
        return json.dumps(graph, cls=PlotlyJSONEncoder)
    else:
        return None


def create_top_companies(df, companies, technology=None):
    df = filter_df(df, technology=technology)
    if len(df) > 0:
        #companies = read_table(schema, 'company', index='id')
        top_companies = df.groupby('company').agg({'description': 'count'})
        top_companies = top_companies.rename(columns={'description': 'vacancies'})

        index_to_company = dict(zip(companies.index, companies['name']))
        top_companies.index = top_companies.index.map(index_to_company)
        top_companies = top_companies[top_companies.index != 'Unknown']

        top_companies = top_companies[top_companies['vacancies'] >= top_companies['vacancies'].mean()]
        top_companies.sort_values(by='vacancies', ascending=True, inplace=True)
        if len(top_companies['vacancies']) > 10:
            top_companies = top_companies[-10:]

        top_layout = go.Layout(
            **layout.to_plotly_json(),
            yaxis=dict(
                ticklabelposition="inside",
                automargin=True
            )
        )

        data = go.Bar(
                x=top_companies["vacancies"],
                y=top_companies.index,
                orientation='h',
                marker=dict(color=top_companies["vacancies"], colorscale=cmap))

        graph = {"data": [data], "layout": top_layout}
        return json.dumps(graph, cls=PlotlyJSONEncoder)
    else:
        return None


def recent_vacancies(df, companies, technology=0, experience=0, work_format=None):
    df = filter_df(df, technology, experience, work_format)
    if len(df) > 0:
        #companies = read_table(schema, 'company', index='id')
        index_to_company = dict(zip(companies.index, companies['name']))

        recent = df.sort_values(by='creation_date', ascending=False)
        if len(recent) > 25:
            recent = recent[:25]

        recent['company'] = recent['company'].map(index_to_company)
        return [{"description": row["description"], "url": row["url"], "company": row["company"]}
                for _, row in recent.iterrows()]
    else:
        return None