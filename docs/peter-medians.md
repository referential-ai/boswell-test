## Peter's original functions 

```python

def medianOfList( lst ) :
    n , srtlst = len( lst ) , sorted( lst )
    return ( ( srtlst[ n // 2 ] + srtlst[ ( n - 1 ) // 2 ] ) / 2 )
def getSingleGrade( g ) :
    d = 0
    if ( g == 'a' ) :  d += 4.
    elif ( g == 'b' ) :  d += 3.
    elif ( g == 'c' ) :  d += 2.
    elif ( g == 'd' ) :  d += 1.
    return ( d )
def getPmGrade( g ) :
    return ( 0.25 if ( g == '+' ) else -0.25 )
def cnvrt2Dgt( grdLst ) :
    gd = [ ]
    for g in grdLst :
        g = g.strip( ).lower( )
        n , d , d2 = len( g ) , 0 , 0
        if ( n >= 1 ) :   d += getSingleGrade( g[ 0 ] )
        if ( n >= 2 and g[ 1 ] != '/' ) :  d += getPmGrade( g[ 1 ] )
        if ( n > 2 and g[ 1 ] == '/' ) :
            if ( n >= 3 ) :    d2 += getSingleGrade( g[ 2 ] )
            if ( n > 3 ) :     d2 += getPmGrade( g[ 3 ] )
            d = ( d + d2 ) / 2
        elif ( n > 2 and g[ 2 ] == '/' ) :
            if ( n >= 4 ) :    d2 += getSingleGrade( g[ 3 ] )
            if ( n > 4 ) :     d2 += getPmGrade( g[ -1 ] )
            d = ( d + d2 ) / 2
        gd.append( d )
    return ( gd )
def medianOfLetterGrades( lst ) :
    dl = cnvrt2Dgt( lst )
    g = medianOfList( dl )
    print( lst , dl , g )
    if ( g >= 4.126 ) :  g = 'A+'
    elif ( g >= 4.01 ) : g = 'A+/A'
    elif ( g >= 3.88 ) : g = 'A'
    elif ( g >= 3.76 ) : g = 'A/A-'
    elif ( g >= 3.51 ) : g = 'A-'
    elif ( g >= 3.26 ) : g = 'A-/B+'
    elif ( g >= 3.126 ) : g = 'B+'
    elif ( g >= 3.01 ) : g = 'B+/B'
    elif ( g >= 2.88 ) : g = 'B'
    elif ( g >= 2.76 ) : g = 'B/B-'
    elif ( g >= 2.51 ) : g = 'B-'
    elif ( g >= 2.26 ) : g = 'B-/C+'
    elif ( g >= 2.126 ) : g = 'C+'
    elif ( g >= 2.01 ) : g = 'C+/C'
    elif ( g >= 1.88 ) : g = 'C'
    elif ( g >= 1.76 ) : g = 'C/C-'
    elif ( g >= 1.51 ) : g = 'C-'
    elif ( g >= 1.26 ) : g = 'C-/D+'
    elif ( g >= 1.126 ) : g = 'D+'
    elif ( g >= 1.01 ) : g = 'D+/D'
    elif ( g >= 0.88 ) : g = 'D'
    elif ( g >= 0.76 ) : g = 'D/D-'
    elif ( g >= 0.51 ) : g = 'D-'
    else : g = 'F'
    return ( g )
medianOfLetterGrades( [ 'A-' , 'A-/B+' , 'A+' , 'B+/B' , 'B-/C+' ] ) , \
medianOfLetterGrades( [ 'A-/B+' , 'A+' , 'B+/B' , 'B-/C+' , 'B' , 'A' ] )
```