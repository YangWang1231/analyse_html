
/*描述一个用户的基本情况*/
create table user(
id integer primary key AUTOINCREMENT,
name text not null
);


/*描述一个被测软件的项目情况*/
create table projects(
    id integer primary key autoincrement,
    projectname text not null,
    userid integer not null,
    projectrowdata Blob not null,    /*用户提交的原始数据：testbed分析的html结果*/
    FOREIGN KEY(userid) REFERENCES user(id)
);



create table GBJ8114_rule(
    id integer primary key autoincrement,
    GJB8114Code text unique,
    Rule_description text not null,
    MandatoryStandard_ch text,    
    /*should be enum (recommended, mandatory), but sqlite has no enum support, 
    this table has to trans another statement when switch to mysql DB engine.
    */
    Rule_classification text check (Rule_classification IN ('RECOMMENDED','MANDATORY', '') )        
);
        
create table LDRA_rule(
    id integer primary key autoincrement,
    LDRACode text unique,
    MandatoryStanard_en text not null
);

create table GJB_LDRA_relation_table(
    id integer primary key autoincrement,
    GJB8114_id integer not null,
    LDRA_id integer not null,
    foreign key(GJB8114_id) references GBJ8114_rule(id)
    foreign key(LDRA_id) references LDRA_rule(id)
);

/*描述一个被测软件的规则违背情况*/
create table rule_obey_info(
    id integer primary key autoincrement,
    projectid integer not null,
    LDRA_Code text not null,
    location_function text not null,
    line_numbers text not null,
    foreign key(projectid) references projects(id)
    /*外键通常是另一个表的主键，但也不是强制的
    但是在目前的场景下不能使用外键，因为LDRA_rule的LDRACode字段不是unique，外键主要是为了保证字段的完整性
    */
    foreign key(LDRA_Code) references LDRA_rule(LDRACode) 
    );

/*描述testbed规则的基本情况，目前仅包含强制类规则*/    
/*
create table LDRA_rule(
    GJB8114Code text primary key,
    LDRACode text UNIQUE, */ /*这个字段可能为空，因为gjb8114的规则在testbed中可能没有对应*/
    /*MandatoryStanard_en text,
    MandatoryStandard_ch text not null,    */
    /*should be enum (recommended, mandatory), but sqlite has no enum support, 
    this table has to trans another statement when switch to mysql DB engine.
    */
    /*Rule_classification text check (Rule_classification IN ('RECOMMENDED','MANDATORY', '') )        
    );*/